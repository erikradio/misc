<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">

        <add>
            <xsl:apply-templates select="@* | node()"/>
        </add>
    </xsl:template>


    <xsl:template match="rec">
        <xsl:for-each select=".">
            <doc>
                <field name="id">
                    <xsl:value-of select="./serno"/>
                </field>
                <field name="title_t">
                    <xsl:value-of select="./title"/>
                </field>
                <field name="date_t">
                    <xsl:value-of select="./date"/>
                </field>
                <field name="author_t">
                    <xsl:value-of select="./author"/>
                </field>
                <field name="documentation_t">
                    <xsl:value-of select="./documentation"/>
                </field>
                <field name="precis_t">
                    <xsl:value-of select="./precis"/>
                </field>

                <xsl:for-each select="tokenize(./persons, '/')">

                    <field name="people_t">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>

                <xsl:for-each select="tokenize(./persons, '/')">

                    <field name="people_facet">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./places, '/')">

                    <field name="place_facet">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./places, '/')">

                    <field name="place_t">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./keyword, '/')">

                    <field name="keyword_facet">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./keyword, '/')">

                    <field name="keyword_t">
                        <xsl:value-of select="."/>

                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./gensubj, '/')">
                    
                    <field name="keyword_t">
                        <xsl:value-of select="."/>
                        
                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./gensubj, '/')">
                    
                    <field name="keyword_facet">
                        <xsl:value-of select="."/>
                        
                    </field>
                </xsl:for-each>
                <field name="first_location">
                    <xsl:value-of select="./firstloc"/>
                    
                </field>
                <field name="original_location">
                    <xsl:value-of select="./orgloc"/>
                    
                </field>
                <field name="other_location">
                    <xsl:value-of select="./othloc"/>
                    
                </field>
                <xsl:for-each select="tokenize(./ethnicgroup, '/')">
                    
                    <field name="ethnic_group_facet">
                        <xsl:value-of select="."/>
                        
                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./ethnicgroup, '/')">
                    
                    <field name="ethnic_group_t">
                        <xsl:value-of select="."/>
                        
                    </field>
                </xsl:for-each>
                <xsl:for-each select="tokenize(./militarygroup, '/')">
                    
                    <field name="military_group_t">
                        <xsl:value-of select="."/>
                        
                    </field>
                </xsl:for-each>
            </doc>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
