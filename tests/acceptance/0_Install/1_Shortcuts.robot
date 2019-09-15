*** Settings ***
Documentation     Do Desktop shortcuts get installed?
Resource          ../../resources/Install.robot

*** Test Cases ***
Are the shortcuts created?
    [Documentation]    Does it cut short?
    Variable Should Exist    ${ROBOTLAB SHORTCUT}    msg=Should have defined shortcut during install
    Wait Until Created    ${FAKE HOME}${/}Desktop${/}${ROBOTLAB SHORTCUT}