$ErrorActionPreference = 'Stop'
$u01Dir = Join-Path $PSScriptRoot 'documents'
$u01Word = New-Object -ComObject Word.Application
$u01Results = @()
try {
    $u01Word.Visible = $false
    $u01Word.DisplayAlerts = 0
    foreach ($u01File in (Get-ChildItem -LiteralPath $u01Dir -Filter '*.docx')) {
        $u01Doc = $u01Word.Documents.Open($u01File.FullName, $false, $true)
        try {
            $u01Doc.Repaginate()
            $u01Pages = $u01Doc.ComputeStatistics(2)
            $u01Rows = 0
            foreach ($u01Table in $u01Doc.Tables) {
                foreach ($u01Row in $u01Table.Rows) {
                    $u01Start = $u01Doc.Range($u01Row.Range.Start, $u01Row.Range.Start)
                    $u01End = $u01Doc.Range($u01Row.Range.End - 2, $u01Row.Range.End - 2)
                    if ($u01Start.Information(3) -ne $u01End.Information(3)) {
                        throw ('Ligne de tableau sur deux pages : ' + $u01File.Name)
                    }
                    $u01Rows++
                }
            }
            $u01Pdf = [System.IO.Path]::ChangeExtension($u01File.FullName, '.pdf')
            $u01Doc.ExportAsFixedFormat($u01Pdf, 17)
            $u01Results += [pscustomobject]@{document=$u01File.Name; pages=$u01Pages; word=$u01Word.Version; lignes_tableaux=$u01Rows; lignes_coupees=0}
            Write-Output ($u01File.Name + ' : ' + $u01Pages + ' pages')
        } finally { $u01Doc.Close(0) }
    }
} finally {
    $u01Word.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($u01Word)
}
$u01Results | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $PSScriptRoot 'controle-word.json')
