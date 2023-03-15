Feature: Delete Posts
  As a user,
  I would like to delete posts

  Scenario: Successfully delete a post
    Given I am on the home page
    And I have created a post
    When I click on the Delete link
    Then the post should disappear
    And a banner should show, saying 'You have delete your post!'
