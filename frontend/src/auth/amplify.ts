import { Amplify } from 'aws-amplify';

const region = import.meta.env.VITE_AWS_REGION || 'us-east-1';
const userPoolId = import.meta.env.VITE_COGNITO_USER_POOL_ID || '';
const userPoolClientId = import.meta.env.VITE_COGNITO_USER_POOL_CLIENT_ID || '';
const domain = import.meta.env.VITE_COGNITO_DOMAIN || '';
const redirectSignIn = import.meta.env.VITE_COGNITO_REDIRECT_SIGN_IN || 'http://localhost:5173/oauth/callback';
const redirectSignOut = import.meta.env.VITE_COGNITO_REDIRECT_SIGN_OUT || 'http://localhost:5173/';

export function configureAuth() {
  Amplify.configure({
    Auth: {
      Cognito: {
        userPoolId,
        userPoolClientId,
        loginWith: {
          oauth: {
            domain,
            scopes: ['email', 'openid', 'profile'],
            redirectSignIn: [redirectSignIn],
            redirectSignOut: [redirectSignOut],
            responseType: 'code',
          },
        },
      },
    },
    region,
  });
}
