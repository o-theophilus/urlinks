<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import Code from '$lib/input_code.svelte';

	import Password from './forgot_3.password.svelte';

	let form = {
		...$module.form
	};
	let error = {};

	const validate_submit = async () => {
		error = {};

		if (!form.code) {
			error.code = 'this field is required';
		} else if (form.code.length != 6) {
			error.code = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Verifying Code . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/2`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module = {
				module: Password,
				form
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Forgot Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Verification Code" error={error.code}>
		<Code bind:value={form.code} />
	</IG>

	<Button primary on:click={validate_submit}
		>Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
