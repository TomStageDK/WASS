<?php

$xsldoc = new DOMDocument();
$xsldoc->load("wass_report.xsl");

$xmldoc = new DOMDocument();
$xmldoc->load("wass_draft.xml");

$proc = new XSLTProcessor();
$proc->importStylesheet($xsldoc);
$html = $proc->transformToXML($xmldoc);
echo $html;

?>