// Tests sans navigateur : direction = vraie variation de coordonnées ; URL locale.
const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const sandbox={window:{}};vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../shared/microduck-sprite.js'),'utf8'),sandbox);
const sprite=sandbox.window.MicroduckSprite;
for (const [dx,dy,dir] of [[1,0,'E'],[-1,0,'O'],[0,1,'S'],[0,-1,'N']]){
 assert.equal(sprite.facing([2,2],[2+dx,2+dy],'E'),dir);
 assert.match(sprite.frame(dir,1),new RegExp('microduck-(north|east|south|west)-1\\.webp$'));
}
assert.equal(sprite.facing([2,2],[2,2],'N'),'N');
assert.equal(sprite.facing([2,2],[4,2],'S'),'S');
assert.equal(sprite.frame('E',-50),'../assets/microduck-east-0.webp');
assert.equal(sprite.frame('O',99),'../assets/microduck-west-2.webp');
console.log('Microduck : 4 directions, immobilité, coordonnées invalides, 3 poses — OK');
