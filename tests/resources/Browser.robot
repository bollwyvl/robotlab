*** Settings ***
Library           JupyterLibrary
Library           OperatingSystem
Resource          Install.robot

*** Variables ***
${NEXT GECKO LOG}   ${0}
${GECKO LOGS}     ${OUTPUT DIR}${/}geckodriver

*** Keywords ***
Open RobotLab
    [Arguments]    ${nbserver}=${None}    ${url}=${EMPTY}    &{configuration}
    [Documentation]    Open RobotLab with the bundled Firefox, served from the
    ...    given (or most-recently-started) ``nbserver`` or ``url``, then wait
    ...    for the splash screen.
    ...    Extra ``configuration`` is passed on to SeleniumLibrary's *Create WebDriver*.
    ${geckodriver} =    Get RobotLab GeckoDriver
    ${firefox} =    Get RobotLab Firefox
    Create Directory    ${GECKO LOGS}
    Create WebDriver    Firefox    executable_path=${geckodriver}    firefox_binary=${firefox}    service_log_path=${GECKO LOGS}${/}${NEXT GECKO LOG}.log    &{configuration}
    Set Global Variable    ${NEXT GECKO LOG}   ${NEXT GECKO LOG.__add__(1)}
    ${nbserver_url} =    Run Keyword If    not "${url}"    Get Jupyter Server URL    ${nbserver}
    ${token} =    Run Keyword If    not "${url}"    Get Jupyter Server Token    ${nbserver}
    ${final_url} =    Set Variable If    "${url}"    ${url}    ${nbserver_url}lab?token=${token}
    Go To    ${final_url}
    Wait for JupyterLab Splash Screen
