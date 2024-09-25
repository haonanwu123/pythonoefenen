# def check_eligibility(age, has_id, member_status):
#  if age >= 18:
#      if has_id:
#          if member_status == "active":
#              return "Eligible for entry"
#          else:
#               return "Membership inactive, not eligible"
#      else:
#           return "No ID, not eligible"
#  else:
#       return "Underage, not eligible"


# The guard clause is a nifty pattern that provides a super-simple way to clean up your code.
# Their main function is to terminate a block of code early,
# which reduces indentation of your code and therefore makes your code much easier to read and reason about.


def check_eligibility(age, has_id, member_status):
    # check is adult or not.
    if age >= 18:
        return "Underage, not eligible"

    # check this person has id or not.
    if not has_id:
        return "No ID, not eligible"

    # check this person is member active or not.
    if not member_status == "active":
        return "Membership inactive, not eligible"

    # all of checks are pass, so this person is eligible.
    return "Eligible for entry"
