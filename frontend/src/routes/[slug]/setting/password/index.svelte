<script>
	import { createEventDispatcher } from 'svelte';

	import Card from '$lib/card.svelte';

	import RequestCode from './1_request_code.svelte';
	import SubmitCode from './2_submit_code.svelte';
	import Password from './3_password.svelte';

	let emit = createEventDispatcher();
	export let open;
	let code;
	let state = 0;
</script>

<Card {open} on:open>
	<svelte:fragment slot="title">Change Password</svelte:fragment>

	{#if state == 0}
		<RequestCode
			on:ok={() => {
				state = 1;
			}}
		/>
	{:else if state == 1}
		<SubmitCode
			on:ok={(e) => {
				code = e.detail;
				state = 2;
			}}
		/>
	{:else if state == 2}
		<Password
			{code}
			on:ok={() => {
				state = 0;
				emit('open', false);
			}}
		/>
	{/if}
</Card>
