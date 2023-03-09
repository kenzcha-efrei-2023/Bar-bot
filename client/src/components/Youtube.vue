<template>
    <div>
        <div style="width:426px;height: 240px;" v-if="rerender">
            <vue-plyr ref="plyr">
                <div data-plyr-provider="youtube" :data-plyr-embed-id="url" ></div>
            </vue-plyr>
        </div>
    </div>
</template>
<script>
import { nextTick } from 'vue';
export default {
    name: 'YoutubeEmbedded',
    props:{
        url : String
    },
    data(){
        return {
            rerender :true 
        }
    },
    watch : {
        url : async function(newValue) {
            this.rerender = false
            await nextTick();
            this.rerender = true
        }
    }
    
}
</script>