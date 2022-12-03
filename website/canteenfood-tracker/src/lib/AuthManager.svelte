<script lang="ts">
  import { Auth } from "aws-amplify";

  let email = "";
  let password = "";
  async function signUp() {
    try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
          email: email,
        },
      });
    } catch (error) {
      console.log("error signing up:", error);
    }
  }

  let confirmEmail = "";
  let confirmCode = "";
  async function confirmSignUp() {
    try {
      await Auth.confirmSignUp(confirmEmail, confirmCode);
    } catch (error) {
      console.log("error confirming sign up", error);
    }
  }

  let singInEmail = "";
  let signInPassword = "";
  async function signIn() {
    try {
      const user = await Auth.signIn(singInEmail, signInPassword);
    } catch (error) {
      console.log("error signing in", error);
    }
  }
</script>

<div class="flex-column m-2">
  <h3>Sign Up</h3>
  <div class="d-flex form-group">
    <input
      bind:value={email}
      type="text"
      class="form-control"
      placeholder="Email" />
    <input
      bind:value={password}
      type="password"
      class="form-control"
      placeholder="Password" />
    <button
      on:click={signUp}
      class="btn btn-primary">Sign Up</button>
  </div>
</div>

<div class="flex-column m-2">
  <h3>Confirm Sign Up</h3>
  <div class="d-flex form-group">
    <input
      bind:value={confirmEmail}
      type="text"
      class="form-control"
      placeholder="Email" />
    <input
      bind:value={confirmCode}
      type="text"
      class="form-control"
      placeholder="Confirmation Code" />
    <button
      on:click={confirmSignUp}
      class="btn btn-primary">Sign Up</button>
  </div>
</div>

<div class="flex-column m-2">
  <h3>Sing In</h3>
  <div class="d-flex form-group">
    <input
      bind:value={singInEmail}
      type="text"
      class="form-control"
      placeholder="Email" />
    <input
      bind:value={signInPassword}
      type="password"
      class="form-control"
      placeholder="Password" />
    <button
      on:click={signIn}
      class="btn btn-primary">Sign In</button>
  </div>
</div>

<style>
   .form-control {
    flex: 1 1 0;
  }
</style>
