<script>
	import { user, organization } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import './layout/var.css';
	import './layout/main.css';
	import Nav from './layout/nav.svelte';
	import Footer from './layout/footer.svelte';
	import Footer2 from './layout/footer2.svelte';

	import Module from './layout/_module.svelte';
	import Loading from './layout/_loading.svelte';
	import Notification from './layout/_notification.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;
	$organization = data.locals.organization;
</script>

<svelte:head>
	{#if $organization.icon}
		<link rel="icon" href={$organization.icon} />
	{:else}
		<link rel="icon" href="/favicon.png" />
	{/if}
</svelte:head>

<main>
	<div class="page">
		<Nav />
		<slot />
		<hr />
		<Footer />
	</div>
	<Footer2 />

	<Module />
	<Loading />
	<Notification />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg1);
		color: var(--ft2);
		transition: background-color var(--trans), color var(--trans);
	}

	.page {
		min-height: 100vh;
	}
</style>
