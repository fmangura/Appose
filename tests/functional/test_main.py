from flask import session

class TestMainBluePrintRoutes():

    def test_GET_home_loggedIn(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and user logged-in
        WHEN GET '/'
        THEN Home template will be successfully loaded
        """
        response = test_client.get('/', follow_redirects=True)
        res = str(response.data)
        assert response.status_code == 200
        assert 'Welcome user1' in res

    def test_GET_home_Fail_Loggin(self, test_client, gen_user):
        """
        GIVEN Flask app
        WHEN GET '/' and NOT logged in
        THEN Landingpage template will be rendered
        """
        # Log In ' redirects to home
        response = test_client.post('/users/login/',
                    data={'username': 'user1',
                            'password': 'INCORRECT'},
                    follow_redirects=True
        )
        res = str(response.data)
        assert 'Failed to Log In!' in res

        # Calling home '/'
        response = test_client.get('/', follow_redirects=True)
        res = str(response.data)
        assert response.status_code == 200
        assert 'You are NOT Signed In' in res

    def test_POST_home(self, test_client, gen_user, log_in):
        """
        GIVEN Flask app and user logged-in
        WHEN POST '/'
        THEN new Post data will be made under the user
        """
        message = 'massa ultricies mi quis hendrerit dolor magna eget est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas integer eget aliquet nibh praesent tristique magna sit amet purus gravida quis blandit turpis cursus in hac TEST NEWLY CREATED POST'
        response = test_client.post('/', data={
                                'user_id': session['curr_user_id'],
                                'message': message,
                                'link':''
                            }, follow_redirects=True)
        res = str(response.data)
        assert response.status_code == 200
        assert 'Welcome user1' in res
        assert 'TEST NEWLY CREATED POST' in res






        


