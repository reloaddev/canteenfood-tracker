import { writable } from 'svelte/store';
import { Auth } from "aws-amplify";

setInterval(function () {
  checkGlobalCurrentUser();
}, 10 * 1000);

export const globalCurrentUser = writable(undefined)
export function checkGlobalCurrentUser() {
  Auth.currentAuthenticatedUser()
    .then((usr) => globalCurrentUser.set(usr))
    .catch(() => globalCurrentUser.set(undefined));
}
checkGlobalCurrentUser();