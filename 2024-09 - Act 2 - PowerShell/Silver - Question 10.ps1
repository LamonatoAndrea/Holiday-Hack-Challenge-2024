$creds = New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force))

$cookieContainer = New-Object System.Net.CookieContainer

$cookie = New-Object System.Net.Cookie
$cookie.Name = "token"
$cookie.Value = "5f8dd236f862f4507835b0e418907ffc"
$cookie.Domain = "127.0.0.1"
$cookieContainer.Add($cookie)

$response = Invoke-WebRequest -Uri http://127.0.0.1:1225/tokens/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C -WebSession (New-Object Microsoft.PowerShell.Commands.WebRequestSession -Property @{ Cookies = $cookieContainer }) -Credential $creds -AllowUnencryptedAuthentication
($response.Content -match "href='([^']+)'") | Out-Null
$mfaCode = $matches[1]

$mfaCookie = New-Object System.Net.Cookie
$mfaCookie.Name = "mfa_token"
$mfaCookie.Value = "$mfaCode"
$mfaCookie.Domain = "127.0.0.1"
$cookieContainer.Add($mfaCookie)

$validateUrl = "http://127.0.0.1:1225/mfa_validate/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C"
Invoke-WebRequest -Uri $validateUrl -WebSession (New-Object Microsoft.PowerShell.Commands.WebRequestSession -Property @{ Cookies = $cookieContainer }) -Credential $creds -AllowUnencryptedAuthentication | select -Expand Content