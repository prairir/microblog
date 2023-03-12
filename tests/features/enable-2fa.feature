Feature: Add tasks to todo list
    As a user,
    I want to be able to have Two factor protection on my account,
    So that I feel safer about my account against potential threats

  Scenario: User visits the 2fa page
    Given the user is on 2fa page
    Then the page should have a text field to enter the phone number for 2fa
    And the page should have a button to enable 2fa