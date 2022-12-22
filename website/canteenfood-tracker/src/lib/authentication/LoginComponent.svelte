<script lang="ts">
  import { Auth } from "aws-amplify";
  import { globalCurrentUser } from "../../store";

  let email = "";
  let password = "";

  async function login() {
    try {
      await Auth.signIn(email, password);
      globalCurrentUser.set(await Auth.currentAuthenticatedUser());
    } catch (error) {
      console.error("error logging in", error);
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
      on:click={login}
      class="btn btn-primary">Sign In</button>
  </div>
</div>

<style>
  .form-control {
    flex: 1 1 0;
  }
</style>
