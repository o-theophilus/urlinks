<script>
	export let href = '';
	export let target = '';
	export let disabled = false;

	export let primary = false;
	export let size = ''; // small, large, wide
	export let extra = ''; // hover_red, outline
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	{target}
	on:click
	{disabled}
	role="presentation"
	class:primary
	class:small={size == 'small'}
	class:large={size == 'large'}
	class:wide={size == 'wide'}
	class={extra}
>
	<slot />
</svelte:element>

<style>
	button,
	a {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp2) var(--sp3);
		border: none;
		border-radius: var(--sp1);
		width: fit-content;

		background-color: var(--button);

		color: var(--ft2_b);
		fill: currentColor;
		text-decoration: none;
		text-align: center;
		font-weight: 800;
		cursor: pointer;

		transition: background-color var(--trans), color var(--trans), opacity var(--trans);
	}

	.large {
		padding: var(--sp2) var(--sp3);
		font-size: 1.2rem;
	}
	.small {
		padding: var(--sp1) var(--sp2);
		gap: var(--sp0);
		font-size: 0.8rem;
		min-width: 28px;
	}
	.wide {
		width: 100%;
	}

	.primary {
		background-color: var(--cl1);
		color: var(--ft1_b);
		box-shadow: 0 -4px 0 var(--cl1_d) inset;
	}

	:disabled {
		box-shadow: unset;

		cursor: unset;
		opacity: 0.2;
	}

	:not(:disabled):hover {
		background-color: var(--cl1);
		color: var(--ft1_b);
	}
	:not(:disabled).primary:hover {
		background-color: var(--cl1_d);
	}

	:not(:disabled):not(.primary).hover_red:hover {
		background-color: var(--cl2);
	}

	:not(:disabled):not(.primary).outline {
		outline: 2px solid var(--overlay);
		outline-offset: -2px;
		transition: outline-color var(--trans);
	}
	:not(:disabled):not(.primary):not(:hover).outline {
		background-color: transparent;
		transition: background-color var(--trans);
	}
	:not(:disabled):not(.primary).outline:hover {
		outline-color: transparent;
	}
</style>
