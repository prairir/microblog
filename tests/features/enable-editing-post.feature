Feature: Allow editing posts
    As a user,
    I want to be able to edit my posts,
    So that I can fix error and better communicate my thoughts,

    Scenario: User visits the edit post page
        Given the user is on the edit post page
        Then the page should have a text field to change their post
        And the page should have a button to submit their changes