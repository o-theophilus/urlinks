<script>
	import { loading, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';

	let emit = createEventDispatcher();
	let form = {};
	let error = {};

	const validate = () => {
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/2`, {
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
			emit('ok', form.code);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	{#if error.error}
		<br />
		<div class="error">
			{error.error}
		</div>
	{/if}

	<br />
	<div class="note">
		Verification Code has been sent to:
		<span>
			{$user.email}
		</span>
	</div>

	<IG name="Verification Code" error={error.code}>
		<Code bind:value={form.code} />
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
		font-size: 0.8rem;
		background-color: var(--bg2);

		border-radius: var(--sp0);
	}

	.note span {
		font-weight: 800;
	}
</style>
