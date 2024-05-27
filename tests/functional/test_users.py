from flask import session

class TestUserBluePrintRoutes():
    def test_GET_login(self, test_client, gen_user):
        """
        GIVEN Flask app
        WHEN GET '/users/login/'
        THEN Login template is received
        """

        response = test_client.get('/users/login/')
        assert response.status_code == 200
        assert b'Welcome back.' in response.data

    def test_POST_login_success(self, test_client, gen_user):
        """
        GIVEN Flask app and correct info
        WHEN POST '/users/login/'
        THEN Home page is rendered along with Success flash message and current user id in session
        """
        response = test_client.post('/users/login/',
                        data={'username': 'user1',
                            'password': 'password'
                            }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Successfully Logged In!' in response.data
        assert b'Welcome user1' in response.data
        assert session['curr_user_id'] == gen_user.id

    def test_POST_login_fail(self, test_client, gen_user):
        """
        GIVEN Flask app and incorrect info
        WHEN POST '/users/login/'
        THEN Failed to Log In message flashes
        """
        response = test_client.post('/users/login/',
                        data={'username': 'user1',
                            'password': 'WRONGWRONG'
                            }, follow_redirects=True)
        
        assert b'Failed to Log In!' in response.data

    def test_GET_logout(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app
        WHEN GET '/users/logout/'
        THEN LandingPage template is rendered instead of home
        """
        # Initially while logged in, home is rendered
        response = test_client.get('/', follow_redirects=True)
        res = str(response.data)
        assert response.status_code == 200
        assert 'Welcome user1' in res

        response = test_client.get('/users/logout/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Successfully Logged Out!' in response.data
        assert b'You are NOT Signed In' in response.data

    def test_GET_userprofile(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and logged in user
        WHEN GET '/users/profile/<id>'
        THEN User's profile will be rendered
        """
        response = test_client.get(f'/users/profile/{gen_user.id}')
        assert response.status_code == 200
        assert gen_user.username in str(response.data)

    def test_GET_userprofile(self, test_client, gen_user, init_database, test_queries, log_in):
        """
        GIVEN Flask app and logged in user
        WHEN GET another user's profile '/users/profile/<id>'
        THEN Another user's profile will show
        """
        user2 = test_queries.get('user2')
        response = test_client.get(f'/users/profile/{user2.id}')
        assert response.status_code == 200
        assert gen_user.username not in str(response.data)
        assert user2.username in str(response.data)

    def test_GET_editprofile(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and logged in
        WHEN GET '/users/<id>/edit'
        THEN A user edit form will be rendered
        """
        response = test_client.get(f'/users/{gen_user.id}/edit')
        assert response.status_code == 200
        assert b'id="editprofile"' in response.data
        assert b'form="editprofile"' in response.data
        assert gen_user.username in str(response.data)

    def test_GET_editprofile_wrongUser(self, test_client, gen_user, init_database, test_queries, log_in):
        """
        GIVEN Flask app and WRONG user logged in
        WHEN GET '/users/<id>/edit'
        THEN A user edit form will be rendered
        """
        user2 = test_queries.get('user2')
        response = test_client.get(f'/users/{user2.id}/edit', follow_redirects=True)
        assert b"You are attempting to access something you are not allowed to." in response.data
        assert b'Welcome user1' in response.data

    def test_POST_editprofile(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and logged in
        WHEN GET '/users/<id>/edit'
        THEN A user edit form will be rendered
        """
        response = test_client.post(f'/users/{gen_user.id}/edit', 
                                    data={
                                            'username': gen_user.username,
                                            'password': gen_user.password,
                                            'bio': 'TEST NEW BIO',
                                            'profile_pic': ''
                                        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'TEST NEW BIO' in response.data

    def test_GET_deleteprofile(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and logged in
        WHEN GET '/users/<id>/DELETE'
        THEN Delete form rendered
        """
        response = test_client.get(f'/users/{gen_user.id}/DELETE', follow_redirects=True)

        assert b"Please enter password to confirm delete." in response.data

    def test_POST_deleteprofile(self, test_client, gen_user):
        """
        GIVEN Flask app and logged in
        WHEN GET '/users/<id>/DELETE'
        THEN user will be deleted and redirected to logout
        """
        response = test_client.post('/users/login/',
                        data={'username': 'user1',
                            'password': 'password'
                            }, follow_redirects=True)
        
        assert response.status_code == 200
        assert session['curr_user_id'] == gen_user.id

        response = test_client.post(f'/users/{gen_user.id}/DELETE',
                                    data={
                                            'username': gen_user.username,
                                            'password': 'password',
                                            'confirm': 'password'
                                        }, follow_redirects=True)

        # Successfully logged out Alert is rendered
        assert b"Successfully Logged Out!" in response.data
        assert b"You are NOT Signed In" in response.data


    
        