<script>
  import { Auth } from "aws-amplify";

  let email = "";
  let password = "";

  async function register() {
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
  async function confirmRegistration() {
    try {
      await Auth.confirmSignUp(confirmEmail, confirmCode);
    } catch (error) {
      console.log("error confirming sign up", error);
    }
  }
</script>

<div class="flex-column mt-1">
  <div class="d-flex form-group gap-1">
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
      on:click={register}
      class="btn btn-primary">Sign Up</button>
  </div>
</div>

<div class="flex-column mt-1">
  <div class="d-flex form-group gap-1">
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
      on:click={confirmRegistration}
      class="btn btn-primary">Sign Up</button>
  </div>
</div>

<style>
  .form-control {
    flex: 1 1 0;
  }
</style>
