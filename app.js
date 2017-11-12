const express = require('express')
const server = express()
const bodyParser = require('body-parser')
const taskQueue = require('seq-queue')
const queue = taskQueue.createQueue(1000)
server.use(bodyParser.json())
server.use(bodyParser.urlencoded({extended:true}))
server.get('/users',(req,res)=>{
    res.json([{name:'Anwesh',age:23},{name:'Anweshe',age:24},{name:'Anweshrt',age:25}])
})
server.post('/send_sms',(req,res)=>{
    console.log(req.body)
    queue.push(function(task){
        const relevant = getRandomRelevance()
        const credit_category = getCreditCategory()
        const personal_account = getPersonalAccountType()
        const currency = getRandomCurrency()
        const type = getRandomType()
        const expense = getRandomExpense()
        res.json({relevant,credit_category,personal_account,currency,type,expense})
        task.done()
    })
})
const getRandomRelevance = ()=>{
    const relvance_array = [true,false]
    return relvance_array[Math.floor(Math.random()*2)]
}
const getRandomType = ()=>{
    const types = ["FOOD","HEALTH","TRANSPORT","SHOPPING","RESIDENCE"]
    return types[Math.floor(Math.random()*types.length)]
}
const getRandomExpense = () => {
    return Math.floor(1000*Math.random())
}
const getRandomCurrency = () => {
    const currencies =  ["INR","DOLLAR","POUND"]
    return currencies[Math.floor(Math.random()*currencies.length)]
}
const getCreditCategory = () => {
    const credit_categories = [true,false]
    return credit_categories[Math.floor(credit_categories.length*Math.random())]
}
const getPersonalAccountType = () => {
    const personal_account_types = [true,false]
    return personal_account_types[Math.floor(personal_account_types.length*Math.random())]
}
server.listen(8000,()=>{
    console.log("started server")
})
