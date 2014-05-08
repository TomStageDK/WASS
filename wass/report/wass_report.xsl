<?xml version="1.0"?>
<!-- =========================================================================
            wass_report.xsl stylesheet version 0.1a
            last change: 2014-04-27
            Tom Stage, http://www.dvos.dk
==============================================================================
    Copyright (c) 2014 Tom Stage
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. The name of the author may not be used to endorse or promote products
       derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
========================================================================== -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output 
	method="html"
	indent="yes"
	encoding="UTF-8"
	version="5.0"
	doctype-system="about:legacy-compat"
/>

<!-- global variables      -->
<!-- ............................................................ -->
<xsl:variable name="wass_report_xsl_version">0.1a</xsl:variable>
<!-- ............................................................ -->
<xsl:variable name="wassversion"><xsl:value-of select="WASS/WASS-version" /></xsl:variable>
<xsl:variable name="wassarguments"><xsl:value-of select="WASS/WASS-arguments" /></xsl:variable>
<xsl:variable name="wassdatetime"><xsl:value-of select="WASS/WASS-Date-time" /></xsl:variable>
<xsl:variable name="wasstarget"><xsl:value-of select="WASS/WASS-Target" /></xsl:variable>
<xsl:variable name="wassdonby"><xsl:value-of select="WASS/WASS-Done-by" /></xsl:variable>
<xsl:variable name="vuln_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability)" /></xsl:variable>
<xsl:variable name="crit_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='CRITICAL'])" /></xsl:variable>
<xsl:variable name="high_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='HIGH'])" /></xsl:variable>
<xsl:variable name="medium_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='MEDIUM'])" /></xsl:variable>
<xsl:variable name="low_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='LOW'])" /></xsl:variable>
<xsl:variable name="info_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='INFORMATIONAL'])" /></xsl:variable>
<xsl:variable name="best_count"><xsl:value-of select="count(WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='BESTPRACTIES'])" /></xsl:variable>
<!-- ............................................................ -->

<!-- root -->
<!-- ............................................................ -->
<xsl:template match="/">
<!-- <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html></xsl:text> -->
<html>
<head>
<xsl:comment>generated with wass_report.xsl - version <xsl:value-of select="$wass_report_xsl_version" /> by Tom Stage - http://www.dvos.dk</xsl:comment>
<link rel="stylesheet" type="text/css" href="./css/wass_report.css"/>
<script src="./javascript/Chart.js"></script>
  <title>WASS Report for: <xsl:value-of select="$wasstarget" /></title>
</head>

<body>
  <div class="coverpage">
	<img src="logo.png" alt="[logo]" />
	<h1>WASS Scan of: <xsl:value-of select="$wasstarget" /></h1>
	<p>
	Was done on <xsl:value-of select="$wassdatetime" /><br />
	And Was done by <xsl:value-of select="$wassdonby" />
	</p>
  </div>
  
	<div class="toc" id="toc-h-1">
	<h1>Table of Contents</h1>
	
	<ul class="toc">
		<li class="frontmatter"><a href="#toc-h-1">Table of Contents</a></li>
		<li class="summary"><a href="#summary-h-1">WASS Summary</a>
		  <ul>
		  <li class="section"><a href="#target-summary">Target Summary</a></li>
		  </ul>
		  <ul>
		  <li class="section"><a href="#overall-summary">Overall Summary</a></li>
		  </ul>
		  <ul>
		  <li class="section"><a href="#vulnerability_summary-h-1">Vulnerabilities Summary</a></li>
		  </ul>
		</li>
		<xsl:if test="$crit_count > 0">
		<li class="critical_vulns"><a href="#critical_vulns">Critical Vulnerabilities</a></li>
		</xsl:if>
		<xsl:if test="$high_count > 0">
		<li class="high_vulns"><a href="#high_vulns">High Vulnerabilities</a></li>
		</xsl:if>
		<xsl:if test="$medium_count > 0">
		<li class="medium_vulns"><a href="#medium_vulns">Medium Vulnerabilities</a></li>
		</xsl:if>
		<xsl:if test="$low_count > 0">
		<li class="low_vulns"><a href="#low_vulns">Low Vulnerabilities</a></li>
		</xsl:if>
		<xsl:if test="$info_count > 0">
		<li class="informational_vulns"><a href="#informational_vulns">Informational Vulnerabilities</a></li>
		</xsl:if>
		<xsl:if test="$best_count > 0">
		<li class="bestpracties_vulns"><a href="#bestpracties_vulns">Best Practies Vulnerabilities</a></li>
		</xsl:if>
	</ul>
	
	</div>

	<div class="summary" id="summary-h-1">
		<h1 class="summary">Summary</h1>
		<h2>WASS Summary</h2>
		<p>The WASS Scan was done on the <xsl:value-of select="$wassdatetime" /><br />
		WASS Version is: <xsl:value-of select="$wassversion" /><br />
		WASS was run with these arguments: <xsl:value-of select="$wassarguments" /><br />
		The WASS target is: <xsl:value-of select="$wasstarget" /><br />
		The WASS scan was done by: <xsl:value-of select="$wassdonby" /> <br />
		The following tools was used in this scan: <br />
		<xsl:for-each select="WASS/Tool-Session" >
			<xsl:value-of select="Tool-name" /><br />
		</xsl:for-each>

		</p>
		
		<div class="section" id="target-summary">
		<h2>Target Summary</h2>
     	<xsl:apply-templates select="WASS/Tool-Session[1]/Site/Host" />
     	<xsl:apply-templates select="WASS/Tool-Session[1]/Site/Host/Port" />
	    <xsl:apply-templates select="WASS/Tool-Session[1]/Site/Host/Port/Service" />
		</div>

		<div class="section" id="overall-summary">
		<h2>Overall Summary</h2>
		<p>
		There are <xsl:value-of select="$vuln_count" /> vulnerabilities found in the application.<br />
		</p>
		</div>
	</div>

	<div class="vulnerability_summary" id="vulnerability_summary-h-1">
		<h1>Vulnerability Summary</h1>
		<xsl:if test="$vuln_count > 0">
			<xsl:if test="$vuln_count = 1">
				<h2>There is <xsl:value-of select="$vuln_count" /> Vulnerability</h2>
		    </xsl:if>
			<xsl:if test="$vuln_count > 1">
				<h2>There are <xsl:value-of select="$vuln_count" /> Vulnerabilities</h2>
		    </xsl:if>
		</xsl:if>
	    <xsl:element name="table">
	      <xsl:attribute name="class">vulnerability_count</xsl:attribute>
	      <xsl:attribute name="id">vulnerability_count</xsl:attribute>
		    <tr class="vulnerability_count">
		        <th class="critical">Critical</th>
		        <th class="high">High</th>
		        <th class="medium">Medium</th>
		        <th class="low">Low</th>
		        <th class="informational">Informational</th>
		        <th class="bestpractice">Best Practice</th>
		      </tr>
		    <tr class="counts">
		        <td class="critical"><xsl:value-of select="$crit_count" /></td>
		        <td class="high"><xsl:value-of select="$high_count" /></td>
		        <td class="medium"><xsl:value-of select="$medium_count" /></td>
		        <td class="low"><xsl:value-of select="$low_count" /></td>
		        <td class="informational"><xsl:value-of select="$info_count" /></td>
		        <td class="bestpractice"><xsl:value-of select="$best_count" /></td>
			</tr>
	    </xsl:element>

		<div class="section" id="vulnerability-chart">
		<xsl:element name="canvas">
		<xsl:attribute name="id">pie</xsl:attribute>
		<xsl:attribute name="height">250</xsl:attribute>
		<xsl:attribute name="width">250</xsl:attribute>
		</xsl:element>
		<script>
	 		var pieData = [
			{
			value: <xsl:value-of select="$crit_count" />,
			color : "#ff0000"
			},
			{
			value : <xsl:value-of select="$high_count" />,
			color:"#8b0000"
			},
			{
			value : <xsl:value-of select="$medium_count" />,
			color : "#ffa500"
			},
			{
			value: <xsl:value-of select="$low_count" />,
			color:"#00bfff"
			},
			{
			value : <xsl:value-of select="$info_count" />,
			color : "#add8e6"
			},
			{
			value : <xsl:value-of select="$best_count" />,
			color : "#F0F8FF"
			}
			];
			
			var myPie = new Chart(document.getElementById("pie").getContext("2d")).Pie(pieData);
		</script>
		</div>
		<div class="critical_summary">
			<h2>There is <xsl:value-of select="$crit_count" /> Critical Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is Critical vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
		<div class="high_summary">
			<h2>There is <xsl:value-of select="$high_count" /> High Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is High vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
		<div class="medium_summary">
			<h2>There is <xsl:value-of select="$medium_count" /> Medium Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is Medium vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
		<div class="low_summary">
			<h2>There is <xsl:value-of select="$low_count" /> Low Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is Low vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
		<div class="info_summary">
			<h2>There is <xsl:value-of select="$info_count" /> Informational Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is Informational vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
		<div class="best_summary">
			<h2>There is <xsl:value-of select="$best_count" /> Best Practies Vulnerabilities</h2>
			<p>
			Is is never a good thing when there is Best Practies vulnerabilities in an Web Application,
			but some may be intentional. But to make sure that this is the case please check the vulnerabilities listed below.  
			</p>
		</div>
	</div>
	
	<div class="critical_vulns" id="critical_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='CRITICAL']" />
	</div>
	
	<div class="high_vulns" id="high_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='HIGH']" />
	</div>
	
	<div class="medium_vulns" id="medium_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='MEDIUM']" />
	</div>
	
	<div class="low_vulns" id="low_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='LOW']" />
	</div>
	
	<div class="informational_vulns" id="informational_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='INFORMATIONAL']" />
	</div>
	
	<div class="bestpracties_vulns" id="bestpracties_vulns">
     <xsl:apply-templates select="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='BESTPRACTIES']" />
	</div>
	
</body>
</html>
</xsl:template>
<!-- ............................................................ -->

<!-- host -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session[1]/Site/Host">
  	<h3>Hostname</h3>
      <ul>
          <li><xsl:value-of select="@name"/></li>
      </ul>
    
    <h3>IP Address</h3>
      <ul>
          <li><xsl:value-of select="@ip-address"/></li>
      </ul>
</xsl:template>
<!-- ............................................................ -->

<!-- ports -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session[1]/Site/Host/Port">
  <h3>Port used in the scan</h3>
      <ul>
          <li>Protocol: <xsl:value-of select="@protocol"/></li>
          <li>Port: <xsl:value-of select="@portid"/></li>
      </ul>
</xsl:template>
<!-- ............................................................ -->

<!-- service -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session[1]/Site/Host/Port/Service">
  <h3>Service</h3>
      <ul>
          <li>Service Name: <xsl:value-of select="@name"/></li>
          <li>Product: <xsl:value-of select="@product"/></li>
          <li>Version: <xsl:value-of select="@version"/></li>
      </ul>
</xsl:template>
<!-- ............................................................ -->

<!-- critical vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='CRITICAL']">
	<xsl:element name="div">
	<xsl:attribute name="class">critical_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">critical</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

<!-- high vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='HIGH']">
	 <xsl:element name="div">
	<xsl:attribute name="class">high_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">high</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

<!-- medium vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='MEDIUM']">
	 <xsl:element name="div">
	<xsl:attribute name="class">medium_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">medium</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

<!-- low vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='LOW']">
	 <xsl:element name="div">
	<xsl:attribute name="class">low_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">low</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

<!-- informational vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='INFORMATIONAL']">
	 <xsl:element name="div">
	<xsl:attribute name="class">informational_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">informational</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

<!-- bestpracties vulnerabilities -->
<!-- ............................................................ -->
<xsl:template match="WASS/Tool-Session/Site/Host/Port/Vulnerability[@Severity='BESTPRACTIES']">
	 <xsl:element name="div">
	<xsl:attribute name="class">bestpracties_vulnerabilities</xsl:attribute>
			<xsl:element name="h2">
			<xsl:attribute name="class">bestpractice</xsl:attribute>
			 		Vulnerability: <xsl:value-of select="Finding/Summary"/>
			</xsl:element>
			<xsl:element name="h3">
			 		This Vulnerability was found by ID: "<xsl:value-of select="Finding/@NativeID"/>" 
			 		and it was found on the <xsl:value-of select="Finding/@IdentifiedTimestamp"/> 
			</xsl:element>
			<xsl:element name="h3">
				Tool Name: <xsl:value-of select="../../../../Tool-name"/>
			</xsl:element>
			<xsl:element name="h3">
				Tool Version: <xsl:value-of select="../../../../Tool-version"/>
			</xsl:element>
			<xsl:element name="h3">
				Vulnerability description:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Description"/>
			</xsl:element>
			<xsl:element name="h3">
				Further info:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Further-info"/>
			</xsl:element>
			<xsl:element name="h3">
				The severity is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Severity"/>
			</xsl:element>
			<xsl:element name="h3">
				The Confidence is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Confidence"/>
			</xsl:element>
			<xsl:element name="h3">
				The Background is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Background"/>
			</xsl:element>
			<xsl:element name="h3">
				The Remediation is:
			</xsl:element>
			<xsl:element name="p">
				<xsl:value-of select="Finding/Remediation"/>
			</xsl:element>
			<xsl:for-each select="Finding/classification" >
				<xsl:element name="h3">
					The classification system is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@type"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					And the classification id is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="@id"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page" >
				<xsl:element name="h3">
					The page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/>
				</xsl:element>
				<xsl:element name="h3">
					The method was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Method"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The URL was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="URL"/>
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Parameters/Parameter" >
				<xsl:element name="h3">
					The parameter used:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="../Parameter"/><br />
				</xsl:element>
			</xsl:for-each>
			<xsl:for-each select="Finding/Pages/Page/Request-response" >
				<xsl:element name="h3">
					The Page reference is:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Page-reference"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Request was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Request"/><br /><br />
				</xsl:element>
				<xsl:element name="h3">
					The Response was:
				</xsl:element>
				<xsl:element name="p">
					<xsl:value-of select="Response"/>
				</xsl:element>
			</xsl:for-each>
	 </xsl:element>
</xsl:template>
<!-- ............................................................ -->

</xsl:stylesheet>
