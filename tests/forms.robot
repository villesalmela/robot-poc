*** Settings ***
Documentation    Testing web forms in the Voting Stats Service application.
Library                               SeleniumLibrary
Library                               Process
Library                               db_library.py    data.db
Suite Setup                           Start App and Open Browser
Suite Teardown                        Terminate App and Close Browser


*** Variables ***
${APP_URL}                          http://127.0.0.1:5000/


*** Test Cases ***
Submit Voter Form
    [Documentation]    Submit voter form and verify the was saved to database correcty.

    Set Test Variable                 ${polling_station_id}              95
    Set Test Variable                 ${polling_station_name}            Pasila
    Set Test Variable                 ${number_of_voters}                3100

    Go To    ${APP_URL}
    Click Link                        link:Log Voters
    Input Text                        id:polling_station_id              ${polling_station_id}
    Input Text                        id:polling_station_name            ${polling_station_name}
    Input Text                        id:number_of_voters                ${number_of_voters}
    Click Button                      id:submit
    Verify Voter Data
    ...    ${polling_station_id}
    ...    ${polling_station_name}
    ...    ${number_of_voters}


Submit Incident Form
    [Documentation]    Submit incident form and verify the was saved to database correcty.

    Set Test Variable                 ${polling_station_id}              95
    Set Test Variable                 ${polling_station_name}            Pasila
    Set Test Variable                 ${incident_type}                   Policy Violation
    Set Test Variable                 ${incident_description}            Voting security compromised

    Go To                             ${APP_URL}
    Click Link                        link:Report Incident
    Input Text                        id:polling_station_id              ${polling_station_id}
    Input Text                        id:polling_station_name            ${polling_station_name}
    Select Radio Button               Incident Type                      ${incident_type}
    Input Text                        id:incident_description            ${incident_description}
    Click Button                      id:submit
    Verify Incident Data
    ...    ${polling_station_id}
    ...    ${polling_station_name}
    ...    ${incident_type}
    ...    ${incident_description}


*** Keywords ***
Start App and Open Browser
    Start Process                     .venv/bin/python     src/app.py    alias=flask
    Sleep                             1
    Set Selenium Speed                0.1
    Open Browser                      ${APP_URL}         Chrome


Terminate App and Close Browser
    Terminate Process                 flask
    Close Browser


Verify Voter Data
    [Arguments]
    ...                               ${polling_station_id}
    ...                               ${polling_station_name}
    ...                               ${number_of_voters}
    
    ${result}=                        Get Voter Data       ${polling_station_id}
    Should Be Equal As Strings        ${result[0]}         ${polling_station_name}
    Should Be Equal As Strings        ${result[1]}         ${number_of_voters}


Verify Incident Data
    [Arguments]                       ${polling_station_id}
    ...                               ${polling_station_name}
    ...                               ${incident_type}
    ...                               ${incident_description}
    
    ${result}=                        Get Incident Data    ${polling_station_id}
    Should Be Equal As Strings        ${result[0]}         ${polling_station_name}
    Should Be Equal As Strings        ${result[1]}         ${incident_type}
    Should Be Equal As Strings        ${result[2]}         ${incident_description}
