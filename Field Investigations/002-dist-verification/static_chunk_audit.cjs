// Parse generated JavaScript without importing or executing the action.
// Run only in the existing isolated dependency container, with network disabled.
const fs = require('node:fs');
const crypto = require('node:crypto');
const ts = require('/work/repo/node_modules/typescript');
const root = '/work/repo/dist';
const result = { kind: 'static-syntax-audit-not-runtime-proof', files: {},
  chunkRequests: [], chunkFilenameAssignments: [], chunkLoaderAssignments: [],
  dynamicImports: [], exportedChunkIds: [], referencesToOldModule: [],
  limitations: ['No action runtime executed',
    'Tracks direct syntax, not aliases, eval, computed property names, or external callers',
    'No claim of general unreachability or absence of vulnerabilities'] };
for (const name of fs.readdirSync(root).filter(n => n.endsWith('.js')).sort()) {
  const text = fs.readFileSync(root + '/' + name, 'utf8');
  const source = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.JS);
  if (source.parseDiagnostics.length) throw new Error('Parse errors in ' + name);
  result.files[name] = { sha256: crypto.createHash('sha256').update(text).digest('hex'),
    bytes: Buffer.byteLength(text) };
  const loc = n => ({ file: name, line: source.getLineAndCharacterOfPosition(n.getStart(source)).line + 1,
    code: n.getText(source) });
  function visit(n) {
    if (ts.isCallExpression(n)) {
      if (n.expression.getText(source) === '__nccwpck_require__.e') {
        const arg = n.arguments[0];
        result.chunkRequests.push({...loc(n),
          literalId: arg && ts.isNumericLiteral(arg) ? Number(arg.text) : null});
      }
      if (n.expression.kind === ts.SyntaxKind.ImportKeyword) result.dynamicImports.push(loc(n));
    }
    if (ts.isBinaryExpression(n) && n.operatorToken.kind === ts.SyntaxKind.EqualsToken) {
      const target = n.left.getText(source);
      if (target === '__nccwpck_require__.u') result.chunkFilenameAssignments.push(loc(n));
      if (target.startsWith('__nccwpck_require__.f.')) result.chunkLoaderAssignments.push(loc(n));
    }
    if (ts.isVariableDeclaration(n) && ['id','ids'].includes(n.name.getText(source))) {
      if (n.parent.parent.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword))
        result.exportedChunkIds.push(loc(n));
    }
    if (ts.isNumericLiteral(n) && n.text === '91184') result.referencesToOldModule.push(loc(n));
    ts.forEachChild(n, visit);
  }
  visit(source);
}
result.requestedLiteralIds = [...new Set(result.chunkRequests.map(x => x.literalId).filter(x => x !== null))].sort((a,b)=>a-b);
result.nonliteralRequestCount = result.chunkRequests.filter(x => x.literalId === null).length;
let oldChunk = fs.readFileSync(root + '/184.index.js', 'utf8');
const substitutions = [['export const id = 184;', 'export const id = 606;'],
  ['export const ids = [184];', 'export const ids = [606];'], ['/***/ 91184:', '/***/ 606:']];
for (const [before, after] of substitutions) {
  if (oldChunk.split(before).length !== 2) throw new Error('Unexpected chunk identity layout');
  oldChunk = oldChunk.replace(before, after);
}
result.oldChunkEqualsCurrentAfterIdentityRenaming =
  oldChunk === fs.readFileSync(root + '/606.index.js', 'utf8');
result.identitySubstitutions = substitutions;
const output = JSON.stringify(result, null, 2) + '\n';
fs.writeFileSync('/work/static-chunk-audit-v2.json', output, {flag:'wx'});
process.stdout.write(output);
