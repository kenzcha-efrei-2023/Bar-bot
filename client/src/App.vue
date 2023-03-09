<template>
  <div id="app">
    <div class="d-flex flex-row">
      <Partition class="p-2 border" v-bind:page_prop="partition"></Partition>
      <div class="p-2 border">
        <Metronome v-bind:mesure="metronome.mesure" v-bind:tempo="metronome.tempo" v-bind:state="metronome.state" v-bind:change_state="metronome.change_state"></Metronome>
       <YoutubeEmbedded v-bind:url="youtube.url"></YoutubeEmbedded>
        <Barbie v-bind:gif="gif_barbie.gif"></Barbie>
        <Subtitles v-bind:content="subtitles"></Subtitles>

      </div>    
    </div>
  </div>
</template>
<script>

  import Barbie from './components/Barbie.vue'
  import Partition from './components/Partition.vue'
  import Metronome from './components/Metronome.vue'
  import YoutubeEmbedded from './components/Youtube.vue'
  import Subtitles from './components/Chat.vue'
  import data from '../../partition/description.json'
  console.log(data)
  const io = require('socket.io-client')
  export default{
    name:'app',
    components:{
      Partition,
      Metronome,
      YoutubeEmbedded,
      Subtitles,
      Barbie
    },
    data(){
      return {
        messages : [],
        subtitles : " ",
        metronome : {mesure : 4, tempo : 120, state:0, change_state:false},
        gif_barbie : {gif : require("./assets/barbieparlepas.gif")}, 
        youtube : {url : this.getYouTubeVideoId("https://www.youtube.com/watch?v=dQw4w9WgXcQ")},
        partition : {next_page : false, prev_page: false,change_part:false,change_page:false,page : 1, id_part:0},
        socket : io('http://localhost:2346', {transports: ['websocket']}
      )
    }
  },
  methods :{
    getYouTubeVideoId : function(url){
      var pattern = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
      var match = url.match(pattern);
      if (match && match[2].length == 11) {
        return match[2];
      } else {
        return null;
      }
    }
  },
  mounted(){
    this.socket.on('message', (sock)=>{
      this.subtitles = sock.content
    })
    this.socket.on('metronome', (sock)=>{
      this.metronome = sock
    })
    this.socket.on("youtube", (sock)=>{
      this.youtube = {url:this.getYouTubeVideoId(sock.url)}
    })
    this.socket.on("start_talking", (sock)=>{
      this.gif_barbie = {gif:require("./assets/barbie.gif")}
    })
    this.socket.on("stop_talking", (sock)=>{
      this.gif_barbie = {gif:require("./assets/barbieparlepas.gif")}
    })
    this.socket.on("partition", (sock)=>{
      this.partition = sock
      if (sock.change_part){
        this.youtube = {url:this.getYouTubeVideoId(data[sock.id_part].url)}
      }
    })
  }
}
</script>