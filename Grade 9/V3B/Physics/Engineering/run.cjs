#!/usr/bin/env node
"use strict";
const fs=require("node:fs"), path=require("node:path");
const load=file=>JSON.parse(fs.readFileSync(path.join(__dirname,file),"utf8"));
const input={registry:load("registry.json"),baseline:load("obligation-baseline.json"),
 bindings:load("topic-bindings.json"),products:load("specimens/products.json"),
 coverage:load("specimens/coverage-baseline.json"),
 documents:Object.fromEntries(["CORE1A","CORE1B","CORE2A","CORE2B"].map(core=>
 [core,fs.readFileSync(path.join(__dirname,"specimens",core+".md"),"utf8")]))};
const command=process.argv[2];
let result;
if(command==="test") result=require("./tests.cjs").run(input);
else if(command==="check"){
 const G=require("./engine/gates.cjs"),P=require("./engine/products.cjs");
 result={topics:input.bindings.map(b=>G.evaluateTopic(input.registry,input.baseline,b)),
 products:input.products.map(p=>({core:p.core,...P.validateProduct(p,input.coverage,[])})),
 personalized_release:"BLOCKED_MISSING_REAL_CALIBRATION",release_authorized:false};
}else{
 process.stderr.write("Usage: node run.cjs check|test\n");process.exit(2);
}
process.stdout.write(JSON.stringify(result,null,2)+"\n");
if(result.status==="FAIL")process.exitCode=1;
