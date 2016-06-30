@echo off
echo Active Directory batch add script...
echo.
set /P ADNum=Number of users to add: %=%
set /P ADUser=Common user name (example: if 'user' then the added users will be 'user1', 'user2', etc): %=%
set /P ADPwd=Initial password: %=%
set /P ADDom=Domain name (example: for mydomain.com, enter 'mydomain'): %=%
set /P ADTld=Top level domain (example: for mydomain.com, enter 'com'): %=%
set /P ADOu=Organizational Unit (example: Users): %=%
cls
echo Config done.
echo Will run dsadd %ADNum% times with the following settings:
echo.
echo OU: cn=%ADUser% (num),ou=%ADOu%,dc=%ADDom%,dc=%ADTld%
echo UPN: %ADUser%(num)@%ADDom%.%ADTld%
echo First name: %ADUser%
echo Last name: (num)
echo Email: %ADUser%(num)@%ADDom%.%ADTld%
echo Initial password: %ADPwd%
echo.
choice /c yn /n /m "Okay [Y/N]?"
set ADChoice=%ERRORLEVEL%
if %ADChoice% EQU 1 (
        FOR /L %%A IN (1, 1, %ADNum%) DO dsadd user "cn=%ADUser% %%A,ou=%ADOu%,dc=%ADDom%,dc=%ADTld%" -upn %ADUser%%%A@%ADDom%.%ADTld% -fn %ADUser% -ln %%A -display "%ADUser% %%A" -pwd %ADPwd% -email %ADUser%%%A@%ADDom%.%ADTld% -disabled no -mustchpwd yes
)
set /P ADdummy=Done. Press ENTER to quit. 
