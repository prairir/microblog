Feature: Archive Posts
  As a user,
  I would like to archive posts
  so i can view the post even if the original post is deleted

  Scenario: Successfully archive a post
    Given that I am logged in
    And I am on the 'Explore' page
    When I click on the 'Archive' link
    Then the link should change to 'Remove from Archive'
    And a banner should show, saying that the post has been 'archived'


  Scenario: Successfully remove an archived post from the explore page
    Given that I am logged in
    And I am on the 'Explore' page
    When I click on the 'Remove from Archive' link
    Then the link should change to 'Archive'
    And a banner should show, saying that the post has been 'removed'


  Scenario: Successfully archive a post
    Given that I am logged in
    And I am on the 'Explore' page
    When I click on the 'Archive' link
    Then the link should change to 'Remove from Archive'
    And a banner should show, saying that the post has been 'archived'


  Scenario: Successfully remove an archived post from the archived page
    Given that I am logged in
    And I am on the 'Profile' page
    When I click View Archived Posts
    And I click Remove from Archive
    Then the archived post should disappear
    And a banner should show, saying that the post has been 'removed'


  Scenario: View archived posts
    Given that I am logged in
    And I am on the 'Profile' page
    When I click View Archived Posts
    Then I should be directed to a page displaying all my archived posts
