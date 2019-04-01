package assignment1;

import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

public class Assignment_1 {

    public static void main(String[] args) {

        try{
            File XmlFile = new File("Assignment_EQ_reduced.xml");
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(XmlFile);

            // normalize CIM XML file
            doc.getDocumentElement().normalize();
            NodeList baseVoltageList = doc.getElementsByTagName("cim:BaseVoltage");

            NodeList substationtList = doc.getElementsByTagName("cim:Substation");
//              <cim:IdentifiedObject.name>Anvers</cim:IdentifiedObject.name>
//		        <entsoe:IdentifiedObject.shortName>Anvers</entsoe:IdentifiedObject.shortName>
//		        <cim:Substation.Region rdf:resource="#_c1d5c0378f8011e08e4d00247eb1f55e"/>

            NodeList voltageLevelList = doc.getElementsByTagName("cim:VoltageLevel");
//              <cim:VoltageLevel rdf:ID="_4ba71b59-ee2f-450b-9f7d-cc2f1cc5e386">
//              <cim:IdentifiedObject.name>10.5</cim:IdentifiedObject.name>
//              <cim:VoltageLevel.lowVoltageLimit>9.450000</cim:VoltageLevel.lowVoltageLimit>
//              <cim:VoltageLevel.highVoltageLimit>11.550000</cim:VoltageLevel.highVoltageLimit>
//              <cim:VoltageLevel.Substation rdf:resource="#_37e14a0f-5e34-4647-a062-8bfd9305fa9d"/>
//              <cim:VoltageLevel.BaseVoltage rdf:resource="#_862a4658-6b03-4550-9de2-b5c413912b75"/>
//              </cim:VoltageLevel>

            NodeList generatingUnitList = doc.getElementsByTagName("cim:GeneratingUnit");
//              <cim:GeneratingUnit rdf:ID="_18993b11-2966-4bce-bab9-d86103f83b53">
//		<cim:IdentifiedObject.name>Gen-1229753060</cim:IdentifiedObject.name>
//		<cim:IdentifiedObject.description>Machine</cim:IdentifiedObject.description>
//		<cim:GeneratingUnit.initialP>90.000000</cim:GeneratingUnit.initialP>
//		<cim:GeneratingUnit.nominalP>255.000000</cim:GeneratingUnit.nominalP>
//		<cim:GeneratingUnit.maxOperatingP>200.000000</cim:GeneratingUnit.maxOperatingP>
//		<cim:GeneratingUnit.minOperatingP>50.000000</cim:GeneratingUnit.minOperatingP>
//		<cim:GeneratingUnit.genControlSource rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#GeneratorControlSource.offAGC"/>
//		<cim:Equipment.aggregate>false</cim:Equipment.aggregate>
//		<cim:Equipment.EquipmentContainer rdf:resource="#_37e14a0f-5e34-4647-a062-8bfd9305fa9d"/>
//	            </cim:GeneratingUnit>

            NodeList synchronousMachineList = doc.getElementsByTagName("cim:SynchronousMachine");
//            <cim:SynchronousMachine rdf:ID="_3a3b27be-b18b-4385-b557-6735d733baf0">
//		<cim:IdentifiedObject.name>BE-G1</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-G1</entsoe:IdentifiedObject.shortName>
//		<cim:IdentifiedObject.description>Machine</cim:IdentifiedObject.description>
//		<cim:Equipment.aggregate>false</cim:Equipment.aggregate>
//		<cim:Equipment.EquipmentContainer rdf:resource="#_4ba71b59-ee2f-450b-9f7d-cc2f1cc5e386"/>
//		<cim:SynchronousMachine.qPercent>50.000000</cim:SynchronousMachine.qPercent>
//		<cim:SynchronousMachine.maxQ>0e+000</cim:SynchronousMachine.maxQ>
//		<cim:SynchronousMachine.minQ>0e+000</cim:SynchronousMachine.minQ>
//		<cim:RotatingMachine.ratedS>300.000000</cim:RotatingMachine.ratedS>
//		<cim:SynchronousMachine.type rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#SynchronousMachineKind.generator"/>
//		<cim:RegulatingCondEq.RegulatingControl rdf:resource="#_6ba406ce-78cf-4485-9b01-a34e584f1a8d"/>
//		<cim:RotatingMachine.GeneratingUnit rdf:resource="#_18993b11-2966-4bce-bab9-d86103f83b53"/>
//		<cim:SynchronousMachine.InitialReactiveCapabilityCurve rdf:resource="#_59ff1e53-0e1a-44c0-ada5-7a0b3a660170"/>
//		<cim:RotatingMachine.ratedU>10.500000</cim:RotatingMachine.ratedU>
//		<cim:RotatingMachine.ratedPowerFactor>0.850000</cim:RotatingMachine.ratedPowerFactor>
//		<cim:SynchronousMachine.shortCircuitRotorType rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#ShortCircuitRotorKind.turboSeries1"/>
//		<cim:SynchronousMachine.r0>0e+000</cim:SynchronousMachine.r0>
//		<cim:SynchronousMachine.r2>0e+000</cim:SynchronousMachine.r2>
//		<cim:SynchronousMachine.x0>0.130000</cim:SynchronousMachine.x0>
//		<cim:SynchronousMachine.x2>0.171000</cim:SynchronousMachine.x2>
//		<cim:SynchronousMachine.earthingStarPointR>0e+000</cim:SynchronousMachine.earthingStarPointR>
//		<cim:SynchronousMachine.earthingStarPointX>0e+000</cim:SynchronousMachine.earthingStarPointX>
//		<cim:SynchronousMachine.r>0e+000</cim:SynchronousMachine.r>
//		<cim:SynchronousMachine.satDirectSubtransX>0.200000</cim:SynchronousMachine.satDirectSubtransX>
//		<cim:SynchronousMachine.satDirectSyncX>2.000000</cim:SynchronousMachine.satDirectSyncX>
//		<cim:SynchronousMachine.satDirectTransX>0e+000</cim:SynchronousMachine.satDirectTransX>
//		<cim:SynchronousMachine.mu>0e+000</cim:SynchronousMachine.mu>
//		<cim:SynchronousMachine.ikk>0e+000</cim:SynchronousMachine.ikk>
//		<cim:SynchronousMachine.voltageRegulationRange>0e+000</cim:SynchronousMachine.voltageRegulationRange>
//		<cim:SynchronousMachine.earthing>true</cim:SynchronousMachine.earthing>
//	        </cim:SynchronousMachine>

            NodeList regulatingControlList = doc.getElementsByTagName("cim:RegulatingControl");
//              <cim:RegulatingControl rdf:ID="_6ba406ce-78cf-4485-9b01-a34e584f1a8d">
//		<cim:IdentifiedObject.name>BE-G1</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-G1</entsoe:IdentifiedObject.shortName>
//		<cim:RegulatingControl.mode rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#RegulatingControlModeKind.voltage"/>
//		<cim:RegulatingControl.Terminal rdf:resource="#_9f5dbaf3-e384-4e86-9d49-f43c30b4e354"/>
//	            </cim:RegulatingControl>

            NodeList powerTransformerList = doc.getElementsByTagName("cim:PowerTransformer");
//            <cim:PowerTransformer rdf:ID="_a708c3bc-465d-4fe7-b6ef-6fa6408a62b0">
//		<cim:IdentifiedObject.name>BE-TR2_1</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-T_1</entsoe:IdentifiedObject.shortName>
//		<cim:IdentifiedObject.description>T1 that is after maintenance</cim:IdentifiedObject.description>
//		<cim:Equipment.aggregate>false</cim:Equipment.aggregate>
//		<cim:Equipment.EquipmentContainer rdf:resource="#_37e14a0f-5e34-4647-a062-8bfd9305fa9d"/>
//		<cim:PowerTransformer.beforeShCircuitHighestOperatingVoltage>0e+000</cim:PowerTransformer.beforeShCircuitHighestOperatingVoltage>
//		<cim:PowerTransformer.beforeShCircuitHighestOperatingCurrent>0e+000</cim:PowerTransformer.beforeShCircuitHighestOperatingCurrent>
//		<cim:PowerTransformer.beforeShortCircuitAnglePf>0e+000</cim:PowerTransformer.beforeShortCircuitAnglePf>
//		<cim:PowerTransformer.highSideMinOperatingU>0e+000</cim:PowerTransformer.highSideMinOperatingU>
//		<cim:PowerTransformer.isPartOfGeneratorUnit>false</cim:PowerTransformer.isPartOfGeneratorUnit>
//		<cim:PowerTransformer.operationalValuesConsidered>false</cim:PowerTransformer.operationalValuesConsidered>
//	            </cim:PowerTransformer>

            NodeList energyConsumerList = doc.getElementsByTagName("cim:EnergyConsumer");
//                <cim:EnergyConsumer rdf:ID="_cb459405-cc14-4215-a45c-416789205904">
//		<cim:IdentifiedObject.name>BE-Load_1</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-L_1</entsoe:IdentifiedObject.shortName>
//		<cim:IdentifiedObject.description>Electrabel</cim:IdentifiedObject.description>
//		<cim:Equipment.aggregate>false</cim:Equipment.aggregate>
//		<cim:Equipment.EquipmentContainer rdf:resource="#_8bbd7e74-ae20-4dce-8780-c20f8e18c2e0"/>
//	            </cim:EnergyConsumer>

            NodeList powerTransformerEndList = doc.getElementsByTagName("cim:PowerTransformerEnd");
//          <cim:PowerTransformerEnd rdf:ID="_49ca3fd4-1b54-4c5b-83fd-4dbd0f9fec9d">
//		<cim:IdentifiedObject.name>BE-TR2_1</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-T_1</entsoe:IdentifiedObject.shortName>
//		<cim:PowerTransformerEnd.r>2.707692</cim:PowerTransformerEnd.r>
//		<cim:PowerTransformerEnd.x>14.518904</cim:PowerTransformerEnd.x>
//		<cim:PowerTransformerEnd.b>0.0</cim:PowerTransformerEnd.b>
//		<cim:PowerTransformerEnd.g>0.0</cim:PowerTransformerEnd.g>
//		<cim:PowerTransformerEnd.r0>2.720000</cim:PowerTransformerEnd.r0>
//		<cim:PowerTransformerEnd.x0>14.516604</cim:PowerTransformerEnd.x0>
//		<cim:PowerTransformerEnd.b0>0.0</cim:PowerTransformerEnd.b0>
//		<cim:PowerTransformerEnd.g0>0.0</cim:PowerTransformerEnd.g0>
//		<cim:TransformerEnd.rground>0e+000</cim:TransformerEnd.rground>
//		<cim:TransformerEnd.xground>0.0</cim:TransformerEnd.xground>
//		<cim:PowerTransformerEnd.ratedS>650.000000</cim:PowerTransformerEnd.ratedS>
//		<cim:PowerTransformerEnd.ratedU>400.000000</cim:PowerTransformerEnd.ratedU>
//		<cim:TransformerEnd.endNumber>1</cim:TransformerEnd.endNumber>
//		<cim:PowerTransformerEnd.phaseAngleClock>0</cim:PowerTransformerEnd.phaseAngleClock>
//		<cim:TransformerEnd.grounded>false</cim:TransformerEnd.grounded>
//		<cim:PowerTransformerEnd.connectionKind rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#WindingConnection.Y"/>
//		<cim:TransformerEnd.BaseVoltage rdf:resource="#_35cf638d-9a9d-4ae5-ae90-2f01ef898cb6"/>
//		<cim:PowerTransformerEnd.PowerTransformer rdf:resource="#_a708c3bc-465d-4fe7-b6ef-6fa6408a62b0"/>
//		<cim:TransformerEnd.Terminal rdf:resource="#_c3774d3f-f48c-4954-a0cf-b4572eb714fd"/>
//	        </cim:PowerTransformerEnd>

            NodeList breakerEndList = doc.getElementsByTagName("cim:Breaker");
//            <cim:Breaker rdf:ID="_38dfcc80-600f-44e2-8f71-fb595b4f00ac">
//		<cim:IdentifiedObject.name>BE_Breaker_1</cim:IdentifiedObject.name>
//		<cim:Equipment.aggregate>false</cim:Equipment.aggregate>
//		<cim:Switch.normalOpen>false</cim:Switch.normalOpen>
//		<cim:Switch.retained>false</cim:Switch.retained>
//		<cim:Equipment.EquipmentContainer rdf:resource="#_8bbd7e74-ae20-4dce-8780-c20f8e18c2e0"/>
//	           </cim:Breaker>

            NodeList ratioTapChangerList = doc.getElementsByTagName("cim:RatioTapChanger");
//            <cim:RatioTapChanger rdf:ID="_955d9cd0-4a10-4031-b008-60c0dc340a07">
//		<cim:IdentifiedObject.name>BE-TR2_2</cim:IdentifiedObject.name>
//		<entsoe:IdentifiedObject.shortName>BE-T_2</entsoe:IdentifiedObject.shortName>
//		<cim:TapChanger.neutralU>220.000000</cim:TapChanger.neutralU>
//		<cim:TapChanger.lowStep>1</cim:TapChanger.lowStep>
//		<cim:TapChanger.highStep>25</cim:TapChanger.highStep>
//		<cim:TapChanger.neutralStep>13</cim:TapChanger.neutralStep>
//		<cim:TapChanger.normalStep>10</cim:TapChanger.normalStep>
//		<cim:RatioTapChanger.stepVoltageIncrement>1.250000</cim:RatioTapChanger.stepVoltageIncrement>
//		<cim:TapChanger.ltcFlag>true</cim:TapChanger.ltcFlag>
//		<cim:TapChanger.TapChangerControl rdf:resource="#_ee42c6c2-39e7-43c2-9bdd-d397c5dc980b"/>
//		<cim:RatioTapChanger.tculControlMode rdf:resource="http://iec.ch/TC57/2013/CIM-schema-cim16#TransformerControlMode.volt"/>
//		<cim:RatioTapChanger.TransformerEnd rdf:resource="#_81a18364-0397-48d3-b850-22a0e34b410f"/>
//	        </cim:RatioTapChanger>

            for (int i = 0; i < baseVoltageList.getLength(); i++) {

                extractNode (baseVoltageList.item(i));
            }

            for (int i = 0; i < substationtList.getLength(); i++) {

                extractNode (substationtList.item(i));
            }


        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void extractNode (Node node){
        // … remember to convert node to element in order to search for the data inside it.
        // element.getElementsByTagName("cim:IdentifiedObject.name").item(0).getTextContent
        //        can be used to read specific attribute of XML node.


        Element element = (Element) node;
        String elementName = element.getTagName();
        String rdfID = element.getAttribute("rdf:ID");
        System.out.println(elementName);



        switch (elementName) {
            case "cim:BaseVoltage":
                String value = element.getElementsByTagName("cim:BaseVoltage.nominalVoltage").item(0).getTextContent();
                System.out.println("rdfID: " + rdfID +"\n" + "Nominal Voltage: " + value +" Volt \n" );
                break;
            case "cim:Substation":
                String name = element.getElementsByTagName("cim:IdentifiedObject.name").item(0).getTextContent();
                Element element1 = (Element) element.getElementsByTagName("cim:Substation.Region").item(0);
                String region_rdf_ID_resource =element1.getAttribute("rdf:resource");
                System.out.println("rdfID: " + rdfID +"\n" + "Name: " + name +" Volt \nRegion : "+ region_rdf_ID_resource +"\n" );
                break;
            case "cim:VoltageLevel":
                System.out.println("Tuesday");
                break;
            case "cim:GeneratingUnit":
                System.out.println("Tuesday");
                break;
            case "cim:SynchronousMachine":
                System.out.println("Tuesday");
                break;
            case "cim:RegulatingControl":
                System.out.println("Tuesday");
                break;
            case "cim:PowerTransformer":
                System.out.println("Tuesday");
                break;
            case "cim:EnergyConsumer":
                System.out.println("Tuesday");
                break;
            case "cim:PowerTransformerEnd":
                System.out.println("Tuesday");
                break;
            case "cim:Breaker":
                System.out.println("Tuesday");
                break;
            case "cim:RatioTapChanger":
                System.out.println("Tuesday");
                break;
        }


    }

}
