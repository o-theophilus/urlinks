<script>
	export let size = 40;
	export let name;
	export let photo;
	export let square = false;

	function hashString(str) {
		let hash = 5381;
		for (let i = 0; i < str.length; i++) {
			hash = (hash << 5) + hash + str.charCodeAt(i);
		}
		return hash;
	}
	$: hue = Math.abs(hashString(name)) % 361;
</script>

{#if photo}
	<img src={`${photo}/${size}` || '/no_photo.png'} alt={name} style:--size="{size}px" class:square />
{:else}
	<div
		class="avatar"
		class:square
		class:light={hue > 29 && hue < 189}
		style:--hue={hue}
		style:--size="{size}px"
	>
		{name[0]}
	</div>
{/if}

<style>
	img,
	.avatar {
		width: var(--size);
		height: var(--size);
		border-radius: 50%;
	}
	.square {
		border-radius: var(--sp1);
	}

	img {
		object-fit: cover;
		display: block;
	}

	.avatar {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		background-color: hsl(var(--hue), 100%, 50%);
		text-transform: capitalize;
		font-size: calc(var(--size) / 3);
		font-weight: bold;

		color: var(--ft1_b);
	}
	.light {
		color: var(--ft1_d);
	}
</style>
