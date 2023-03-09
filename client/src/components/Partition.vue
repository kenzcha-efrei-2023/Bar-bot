<template>
<div class="row border" style="max-width: 60%">
    <div  class="col-3 " id="test" style="padding-top: 2%;" >
        <h4 class="text-center">
            Partition
        </h4>
        <div  id="scrollable">
            <ul class="list-group list-group-flush" v-for="partition in partitions">
                <li class="list-group-item" v-on:click="select_partition(partition)">{{ partition.title }}</li>
            </ul>
        </div>
            <div class="input-group" style="margin-left: 20%;">
                <button class="btn btn-outline-secondary" type="button" v-on:click="prev_page"><</button>
                <p class="m-2">Page {{ page }}</p>
                <button class="btn btn-outline-secondary" type="button"  v-on:click="next_page">></button>
            </div>
    </div>
    <div class="col border width-2 ">
        <img :src= "require(`../../../partition/${source_partition}`)"  class="img-fluid" alt="Responsive image" style="max-width:100%; min-width: 100%;">
    </div>
</div>
</template>
<style>
#scrollable{
    max-height: 250px;
    margin-bottom: 10px;
    overflow:scroll;
}
#test{
    text-align: center;
}
</style>
<script>

    export default {
    name: 'Partition',
    data() {
      return {
        partitions : {
            0 : {id:0, title : "clair-de-lune" ,nb_page : 6},
            1 : {id:1, title : "la-belle-au-bois-dormant"  , nb_page : 6},
            2 : {id:2, title : "nuages", nb_page : 21}
        },
        active_partition : {id:-1},
        source_partition : "placeholder/image/placeholder.png",
        page : 0
      };
    },
    props : {
        page_prop : Object,
    },
    methods:{
        select_partition: function(name){
            this.active_partition = name
            this.page=1
            this.print_page()
        },
        select_page : function(num){
            if (num > 0 && num <= this.active_partition.nb_page)
            this.page = num
            this.print_page()
        },
        next_page : function(){
            if (this.active_partition.id > -1){
                if (this.page < this.active_partition.nb_page){
                    this.select_page(this.page + 1)
                }
            }
        },
        prev_page : function(){
            if (this.active_partition.id > -1){
                if (this.page > 1){
                    this.select_page(this.page - 1)
                }
            }
        },
        print_page : function(){
            if (this.active_partition.id > -1){
                this.source_partition = this.active_partition.title + "/image/" + this.page.toString() + ".png"
            }
        }  
    },
    watch:{
        page_prop(newValue){
            if (newValue.change_part){
                this.select_partition(this.partitions[newValue.id_part])
            }
            else if (newValue.prev_page){
                this.prev_page()
            }
            else if (newValue.next_page){
                this.next_page()
            }
            if (newValue.change_page){
                this.select_page(newValue.page)
            }
        }
    },
    mounted(){
    }
}
</script>