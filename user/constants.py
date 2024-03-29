REGION_CHOICE = (
        ("서울", "서울"), ("경기", "경기"), ("인천", "인천"), ("세종", "세종"), ("강원", "강원"), 
        ("충북", "충북"), ("충남", "충남"), ("전북", "전북"), ("전남", "전남"), ("광주", "광주"), 
        ("대전", "대전"), ("대구", "대구"), ("부산", "부산"), ("울산", "울산"), ("제주", "제주")
)    


TIME_CHOICE = (
        ("주중 선호", "주중 선호"), ("주말 선호", "주말 선호"), ("상관없음", "상관없음")
)

SKILLS_CHOICE = (
(".NET",".NET"),
("ABAP","ABAP"),
("AIX","AIX"),
("ASP","ASP"),
("ASP.NET","ASP.NET"),
("AWS","AWS"),
("Ajax","Ajax"),
("Android","Android"),
("Angular","Angular"),
("Apache","Apache"),
("ArcGIS","ArcGIS"),
("Azure","Azure"),
("Bootstrap","Bootstrap"),
("C#","C#"),
("C++","C++"),
("COBOL","COBOL"),
("CSS","CSS"),
("CSS3","CSS3"),
("CentOS","CentOS"),
("C언어","C언어"),
("Delphi","Delphi"),
("Directx","Directx"),
("Django","Django"),
("Docker","Docker"),
("ECMAScript","ECMAScript"),
("Eclipse","Eclipse"),
("ElasticStack","ElasticStack"),
("FLEX","FLEX"),
("Flask","Flask"),
("Flutter","Flutter"),
("GCP","GCP"),
("Git","Git"),
("GoLang","GoLang"),
("GraphQL","GraphQL"),
("Groovy","Groovy"),
("Gulp","Gulp"),
("HBase","HBase"),
("HTML","HTML"),
("HTML5","HTML5"),
("Hadoop","Hadoop"),
("IaaS","IaaS"),
("Ionic","Ionic"),
("JPA","JPA"),
("JSP","JSP"),
("Java","Java"),
("Javascript","Javascript"),
("Jenkins","Jenkins"),
("Kafka","Kafka"),
("Keras","Keras"),
("Kotlin","Kotlin"),
("Kubernetes","Kubernetes"),
("LabVIEW","LabVIEW"),
("Linux","Linux"),
("Logstash","Logstash"),
("Lucene","Lucene"),
("MFC","MFC"),
("MSSQL","MSSQL"),
("MacOS","MacOS"),
("MariaDB","MariaDB"),
("Matlab","Matlab"),
("Maven","Maven"),
("MongoDB","MongoDB"),
("MyBatis","MyBatis"),
("MySQL","MySQL"),
("NoSQL","NoSQL"),
("Node.js","Node.js"),
("OSS","OSS"),
("Objective-C","Objective-C"),
("OpenCV","OpenCV"),
("OpenGL","OpenGL"),
("OracleDB","OracleDB"),
("PHP","PHP"),
("PL/SQL","PL/SQL"),
("PaaS","PaaS"),
("Pandas","Pandas"),
("Perl","Perl"),
("PostgreSQL","PostgreSQL"),
("Pro-C","Pro-C"),
("Python","Python"),
("Pytorch","Pytorch"),
("QGIS","QGIS"),
("Qt","Qt"),
("R","R"),
("React","React"),
("React-Native","React-Native"),
("ReactJS","ReactJS"),
("Redis","Redis"),
("Redux","Redux"),
("RestAPI","RestAPI"),
("Ruby","Ruby"),
("SAS","SAS"),
("SQL","SQL"),
("SQLite","SQLite"),
("SVN","SVN"),
("SaaS","SaaS"),
("Scala","Scala"),
("Servlet","Servlet"),
("Solaris","Solaris"),
("Solidity","Solidity"),
("Spark","Spark"),
("Splunk","Splunk"),
("Spring","Spring"),
("SpringBoot","SpringBoot"),
("Storm","Storm"),
("Struts","Struts"),
("Swift","Swift"),
("Sybase","Sybase"),
("Tensorflow","Tensorflow"),
("Tomcat","Tomcat"),
("TypeScript","TypeScript"),
("Ubuntu","Ubuntu"),
("Unity","Unity"),
("Unix","Unix"),
("Unreal","Unreal"),
("VB.NET","VB.NET"),
("Verilog","Verilog"),
("Vert.x","Vert.x"),
("VisualBasic","VisualBasic"),
("VisualC·C++","VisualC·C++"),
("Vue.js","Vue.js"),
("WAS","WAS"),
("WPF","WPF"),
("WebGL","WebGL"),
("WebRTC","WebRTC"),
("Webpack","Webpack"),
("XML","XML"),
("iBATIS","iBATIS"),
("iOS","iOS"),
("jQuery","jQuery"),
)

if __name__ == "__main__":
        for i in SKILLS_CHOICE:
                print(i[0])