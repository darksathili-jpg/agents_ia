const assert = require('node:assert/strict');
const E = require('../../shared/editor-indent.js');
let n=0;
function test(name,actual,expect){assert.equal(actual,expect,name);n++;}
function testRes(name,data,expected,caret){test(name,data.value,expected); if(caret!==undefined){test(name+' caret',data.start,caret);}}
testRes('Enter after def',E.enter('def f():',8,8),'def f():\n    ',13);
testRes('Nested if',E.enter('def f():\n    if x:',18,18),'def f():\n    if x:\n        ',27);
testRes('After return',E.enter('    return 4',12,12),'    return 4\n    ');
testRes('Tab inserts 4 spaces',E.indent('x',1,1),'x    ',5);
testRes('Backspace removes indent',E.backspace('        x',8,8),'    x',4);
testRes('Two lines indent',E.indent('x\ny',0,3),'    x\n    y');
testRes('Two lines unindent',E.unindent('    x\n    y',0,11),'x\ny');
testRes('Single shift tab',E.unindent('    x',4,4),'x');
testRes('Selection replacement enter',E.enter('def f(): abc',9,12),'def f(): \n    ');
console.log(`OK : ${n} assertions sur l’indentation et les sélections.`);
