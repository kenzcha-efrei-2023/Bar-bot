<template>
    <div class="border">
        <p>
            {{ content }}
        </p>
    </div>
</template>
<script>
export default {
    name : "Subtitles",
    props: {content:String},
    data() {
        return{
        }
    }
}
</script>
