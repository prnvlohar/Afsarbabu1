# from datetime import datetime
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# from django.conf import settings
# from django.utils.crypto import constant_time_compare, salted_hmac
# from django.utils.http import base36_to_int, int_to_base36


# class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
#     """
#     Strategy object used to generate and check tokens for the password
#     reset mechanism.
#     """

#     def make_token(self, user):
#         """
#         Return a token that can be used once to do a password reset
#         for the given user.
#         """
#         # breakpoint()
#         return self._make_token_with_timestamp(
#             user,
#             self._num_seconds(self._now()),
#             self.secret,
#         )

#     def check_token(self, user, token):
#         """
#         Check that a password reset token is correct for a given user.
#         """
#         if not (user and token):
#             return False
#         # Parse the token
#         print("***********")
        
#         try:
#             ts_b36, _ = token.split("-")
#         except ValueError:
#             return False
#         print("***********ts_b36", ts_b36, _)
#         try:
#             ts = base36_to_int(ts_b36)
#         except ValueError:
#             return False

#         print("*******ts", ts)
#         # Check that the timestamp/uid has not been tampered with
#         for secret in [self.secret, *self.secret_fallbacks]:
#             breakpoint()
#             if constant_time_compare(
#                 self._make_token_with_timestamp(user, ts, secret),
#                 token,
#             ):
#                 print("********* constant_time_compare")
#                 break
#         else:
#             print("********* constant_time_compare False")
#             # return False
        
#         breakpoint()
#         print("settings.PASSWORD_RESET_TIMEOUT****", settings.PASSWORD_RESET_TIMEOUT)
#         print("self._num_seconds(self._now()) - ts", self._num_seconds(self._now()) - ts)
        
#         # Check the timestamp is within limit.
#         if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
#             print("&&&&&&&&&&&")
#             return False

#         return True

    
# custom_default_token_generator = CustomPasswordResetTokenGenerator()
