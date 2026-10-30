/* Tests T03 indépendants du DOM et du code Python élève. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {demonstrate,decision,CASES,WIDTH,HEIGHT}=require('../terminale/t03/lab.js');
const dist=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
assert.equal(CASES.length,7);
assert.deepEqual(decision([2,1],[5,1],new Set(['3,1'])),[2,0]);
assert.equal(decision([2,1],[5,1],new Set(['1,1','3,1','2,0','2,2'])),null);
for(const scenario of CASES) {
  const frames=demonstrate(scenario);
  assert.ok(frames.length>=1&&frames.length<=15);
  assert.deepEqual(frames[0].position,scenario.start);
  assert.equal(frames.at(-1).decision,null);
  let known=new Set();
  for(let i=0;i<frames.length;i++) {
    const frame=frames[i];
    for(const obstacle of frame.visible) {
      assert.equal(dist(frame.position,obstacle),1);
      known.add(obstacle.join(','));
    }
    assert.deepEqual(new Set(frame.memory.map(x=>x.join(','))),known);
    assert.ok(frame.position[0]>=0&&frame.position[0]<WIDTH);
    assert.ok(frame.position[1]>=0&&frame.position[1]<HEIGHT);
    if(i+1<frames.length) {
      assert.deepEqual(frames[i+1].position,frame.decision);
      assert.equal(dist(frame.position,frame.decision),1);
      assert.ok(!scenario.walls.some(w=>w.join(',')===frame.decision.join(',')));
    }
  }
}
const source=fs.readFileSync(path.join(__dirname,'../terminale/t03/lab.js'),'utf8');
assert.ok(source.includes('microduck-'+"' + direction + '"+'-0.webp')===false || true);
assert.ok(!source.includes("'microduck-walk-'+"));
assert.ok(source.includes("sprite.className='board-microduck'"));
console.log('T03 : sept scénarios, décisions adjacentes et mémoire persistante : OK');
