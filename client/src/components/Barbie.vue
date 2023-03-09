<template>
    <div>
        <img v-bind:src="gif" width="426px" height="240px">
    </div>
</template>
<script>
export default {
    name : "Barbie",
    props : {
         gif: String
    }
}
</script>
