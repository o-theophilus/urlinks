<script>
	import { module, loading, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Password from './password_checker.svelte';
	import Login from './login.svelte';
	import ShowPassword from './password_show.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let show_password = false;

	let form = {
		email: $module.email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.firstname) {
			error.firstname = 'this field is required';
		}
		if (!form.lastname) {
			error.lastname = 'this field is required';
		}
		if (!form.email) {
			error.email = 'this field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		} else if (
			$organization.email_domains.length > 0 &&
			!$organization.email_domains.some((x) => form.email.endsWith(x))
		) {
			error.email = `invalid ${$organization.name} email`;
		}

		if (!form.password) {
			error.password = 'this field is required';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'this field is required';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'does not match password';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'Loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/signup`, {
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
				module: Confirm,
				email: form.email
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Signup </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Firstname"
		icon="person"
		error={error.firstname}
		placeholder="Firstname here"
		type="text"
		bind:value={form.firstname}
	/>
	<IG
		name="Lastname"
		icon="person"
		error={error.lastname}
		placeholder="Lastname here"
		type="text"
		bind:value={form.lastname}
	/>
	<IG
		name="Email"
		icon="email"
		error={error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
	/>
	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.password}
	>
		<svelte:fragment slot="right">
			<div class="right">
				<ShowPassword bind:show_password />
			</div>
		</svelte:fragment>
		<svelte:fragment slot="down">
			<Password password={form.password} />
		</svelte:fragment>
	</IG>
	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		placeholder="Password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.confirm_password}
	/>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />

	<Link
		on:click={() => {
			$module = {
				module: Login,
				email: form.email
			};
		}}
	>
		Login
	</Link>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
	.right {
		padding-right: var(--sp2);
	}
</style>
