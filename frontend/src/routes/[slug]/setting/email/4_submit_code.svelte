<script>
	import { user, notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';

	let emit = createEventDispatcher();
	export let code_1;
	export let email;
	let form = {
		code_1: code_1,
		email: email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'this field is required';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid verification code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Verifying Code / Saving Email . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			$user = resp.user;

			$notification = {
				message: 'Email changed'
			};

			emit('ok');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div class="note">
		Verification Code has been sent to:
		<span>
			{form.email}
		</span>
		.
	</div>

	<IG name="Verification Code" error={error.code_2}>
		<Code bind:value={form.code_2} />
	</IG>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	.error {
		margin: var(--sp2) 0;
	}

	.note {
		padding: var(--sp2);
		margin: var(--sp2) 0;
		font-size: 0.8rem;
		background-color: var(--bg2);

		border-radius: var(--sp0);
	}

	.note span {
		font-weight: 800;
	}
</style>
