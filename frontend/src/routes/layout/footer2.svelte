<script>
	import { organization } from '$lib/store.js';
</script>

{#if $organization.fullname}
	<div class="copyright">
		<div class="block">© 2024 | {$organization.fullname}</div>
	</div>
{/if}

<style>
	.block {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.copyright {
		padding: var(--sp4) 0;

		text-align: center;
		color: var(--ft1_b);
		font-size: 0.8rem;
		background-color: var(--ft1_d);
	}
</style>
