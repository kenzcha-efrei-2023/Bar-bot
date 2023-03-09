<template>
    <div>
        <div class="d-flex flex-row" style="width:fit-content; height: fit-content;">
        <img src="../assets/metronome.png" width="50px" height="50px" class= "p-2">
        <div class="input-group p-2" style="height: 50px; width: 200px;">
            <input type="text" class="form-control " placeholder="100" aria-label="Recipient's username" aria-describedby="basic-addon2" v-model="temp">
            <div class="input-group-append ">
                <button class="btn btn-outline-secondary" type="button" v-on:click="add_tempo">+</button>
                <button class="btn btn-outline-secondary" type="button" v-on:click="rem_tempo">-</button>
            </div>
        </div>
        <div class="d-flex flex-row p-2" style="height: 50px; width">
        <div class="input-group input-group-sm mb-3">
        <div class="input-group-prepend">
            <span class="input-group-text" id="inputGroup-sizing-sm">Mesure</span>
        </div>
        <input type="number" class="form-control btn-outline-secondary" aria-label="Small" aria-describedby="inputGroup-sizing-sm" v-model="mes" v-on:change="change_mesure">
        </div>
    </div>
        <div class="p-2">
            <button type="button" class="btn btn-outline-secondary" v-on:click="invert_state">{{ states[stat] }}</button>
        </div>
    
    </div>
    </div>

</template>
<script>
import Metronome_obj from './metronome_obj'
var metron = new Metronome_obj();
metron.tempo = 100

export default {
    props:{mesure : Number, tempo : Number, state: Number, change_state : Boolean},
    name: 'Metronome',
    data() {
      return {
        mes : 4,
        temp : 100,
        states : ["Off", "On"],
        stat : 0
      }},
      mounted : function(){
        this.temp =  this.tempo
        this.mes =  this.mesure
        this.stat = this.state
      },
      watch:{
        mesure(newValue){
            if (!this.change_state){
                this.mes = newValue
                metron.beatsPerBar = this.mes
            }
        },
        tempo(newValue){
            if (!this.change_state){
                this.temp = newValue
                metron.tempo = this.temp
            }
        },
        state(newValue){
            if (this.change_state && newValue != this.stat)
                this.stat = newValue
                metron.startStop()
        }
      },
      methods:{
        add_tempo : function(){
            this.temp = parseInt(this.temp) + 5
            metron.tempo = this.temp
        },
        rem_tempo : function(){
            this.temp = parseInt(this.temp) - 5
            metron.tempo = this.temp
        },
        set_tempo : function(num){
            metron.tempo = num
            this.temp = num
        },
        invert_state : function(){
            this.stat = (this.stat+1)%2
            metron.startStop()
        },
        change_mesure : function(){
            metron.beatsPerBar = this.mes
        }
      }
}

</script>