$(document).ready(function() {
  $('.ui.form')
    .form({
      fields: {
        username: {
          identifier  : 'username',
          rules: [
            {
              type   : 'empty',
              prompt : 'Please enter your username'
            }
          ]
        },
        email: {
          identifier  : 'email',
          rules: [
            {
              type   : 'empty',
              prompt : 'Please enter your email'
            },
            {
              type   : 'email',
              prompt : 'Please enter a valid email'
            }
          ]
        },
        password: {
          identifier  : 'password',
          rules: [
            {
              type   : 'empty',
              prompt : 'Please enter your password'
            },
            {
              type   : 'length[6]',
              prompt : 'Your password must be at least 6 characters'
            }
          ]
        },
        terms: {
          identifier: 'terms',
          rules: [
            {
              type   : 'checked',
              prompt : 'You must agree to the terms and conditions'
            }
          ]
        }
      }
    })
  ;
})
;