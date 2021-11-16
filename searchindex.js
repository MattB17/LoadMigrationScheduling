Search.setIndex({docnames:["Data/constraint_dict","Data/controller_constraint","Data/data","Data/instance_data","Data/migration","Data/qos_constraint","Data/simulator","Model/model","Model/optimizer","Model/parser","Model/round","algorithms","exceptions","index","utils"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["Data/constraint_dict.rst","Data/controller_constraint.rst","Data/data.rst","Data/instance_data.rst","Data/migration.rst","Data/qos_constraint.rst","Data/simulator.rst","Model/model.rst","Model/optimizer.rst","Model/parser.rst","Model/round.rst","algorithms.rst","exceptions.rst","index.rst","utils.rst"],objects:{"MigrationScheduling.Data":{ConstraintDict:[0,0,0,"-"],ControllerConstraint:[1,0,0,"-"],Migration:[4,0,0,"-"],QosConstraint:[5,0,0,"-"],Simulator:[6,0,0,"-"]},"MigrationScheduling.Data.ConstraintDict":{get_capacity:[0,2,1,""],get_load:[0,2,1,""],get_load_factor:[0,2,1,""],get_switches:[0,2,1,""],remove_switch:[0,2,1,""]},"MigrationScheduling.Data.ControllerConstraint":{add_switch:[1,2,1,""],get_cap:[1,2,1,""],get_constraint_dict:[1,2,1,""],get_controller:[1,2,1,""],get_controller_idx:[1,2,1,""],get_switches:[1,2,1,""],get_total_load:[1,2,1,""]},"MigrationScheduling.Data.Migration":{add_qos_group:[4,2,1,""],get_dst_controller:[4,2,1,""],get_groups:[4,2,1,""],get_load:[4,2,1,""],get_switch:[4,2,1,""],get_switch_idx:[4,2,1,""],is_in_group:[4,2,1,""]},"MigrationScheduling.Data.QosConstraint":{add_switch:[5,2,1,""],get_cap:[5,2,1,""],get_constraint_dict:[5,2,1,""],get_group:[5,2,1,""],get_group_idx:[5,2,1,""],get_switches:[5,2,1,""]},"MigrationScheduling.Data.Simulator":{run:[6,2,1,""]},"MigrationScheduling.Model":{Optimizer:[8,0,0,"-"],Parser:[9,0,0,"-"],Round:[10,0,0,"-"]},"MigrationScheduling.Model.Optimizer":{build_ip_model:[8,2,1,""],build_lp_model:[8,2,1,""],get_model_bounds:[8,2,1,""],get_model_data:[8,2,1,""],instance_data:[8,2,1,""]},"MigrationScheduling.Model.Parser":{get_controller_constraints:[9,2,1,""],get_controller_ids:[9,2,1,""],get_group_ids:[9,2,1,""],get_migrations:[9,2,1,""],get_qos_constraints:[9,2,1,""],get_switch_ids:[9,2,1,""],parse_migrations:[9,2,1,""],to_data:[9,2,1,""]},"MigrationScheduling.Model.Round":{can_schedule_migration:[10,2,1,""],print_migrations:[10,2,1,""],schedule_migration:[10,2,1,""]},"MigrationScheduling.algorithms":{current_bottleneck_first:[11,3,1,""],find_scheduling_round:[11,3,1,""],get_bottleneck_constraint:[11,3,1,""],remove_migration_from_constraints:[11,3,1,""],select_migration_from_constraint:[11,3,1,""],vector_first_fit:[11,3,1,""]},"MigrationScheduling.exceptions":{InstanceNotSpecified:[12,4,1,""],InvalidName:[12,4,1,""],ModelNotOptimized:[12,4,1,""],UninitializedModel:[12,4,1,""]},"MigrationScheduling.utils":{get_cap_dicts:[14,3,1,""],get_constraint_dicts:[14,3,1,""],get_controller_cap_dict:[14,3,1,""],get_controller_constraint_dicts:[14,3,1,""],get_qos_constraint_dicts:[14,3,1,""],get_qos_group_cap_dict:[14,3,1,""],upper_bound_rounds:[14,3,1,""]},MigrationScheduling:{Data:[2,0,0,"-"],Model:[7,0,0,"-"],algorithms:[11,0,0,"-"],exceptions:[12,0,0,"-"],utils:[14,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:exception"},terms:{"class":[0,1,2,4,5,6,7,8,9,10,12],"float":[0,1,4,6,10,14],"function":13,"int":[1,4,5,6,8,10,11,14],"new":11,"return":[0,1,4,5,6,8,9,10,11,14],"switch":[0,1,2,5,9,13],"true":[4,10],"while":[1,5],A:[0,1,2,4,5,6,7,8,9,10,11,12,14],At:11,For:11,If:[8,11],In:11,It:[0,1],That:0,The:[0,1,4,5,6,8,9,10,11,12,14],_capac:[0,1,5],_control:[1,6],_controller_const:[],_controller_constraint:9,_controller_id:[],_data:8,_dst_control:4,_group:[4,5],_load:[0,4],_migrat:[6,9,10],_model:8,_num_control:6,_num_migr:6,_num_qos_group:6,_qos_const:[],_qos_constraint:9,_qos_group:6,_qos_id:[],_rem_controller_cap:10,_rem_qos_cap:10,_round_id:[],_round_num:10,_switch:[0,1,4,5],_switch_id:[],about:10,access:12,accommod:[1,5,14],accomod:11,account:10,across:[0,1],ad:[4,5,11],add:[1,4,5],add_qos_group:4,add_switch:[1,5],addit:11,after:[10,11],algorithm:[13,14],all:[0,1,2,7,8,11],allow:[5,11,14],alreadi:11,among:11,amount:[10,14],an:[1,4,5,6,8,9,10,11,12,14],ani:11,anoth:11,appear:0,appli:[1,5],ar:[1,9,10,11,14],associ:[0,14],attribut:[0,1,4,5,6,8,9,10],base:[1,8,14],been:[8,11,12],being:[0,4,8,10],belong:[4,6],bin:11,bool:[4,10],both:14,bottleneck:11,bound:[8,14],build:[1,8,12,14],build_ip_model:8,build_lp_model:8,built:[9,14],calcul:1,can:[5,10,11,14],can_schedule_migr:10,cannot:11,capac:[0,1,5,10,11,14],capciti:10,check:4,chosen:11,collect:[0,1,4,5,9,11,14],compact:[1,5],complet:[1,8,10,14],comput:8,concurr:5,consist:14,constraint:[2,9,11,13,14],constraint_dict:11,constraintdict:[0,1,5,11,14],construct:[8,14],contain:[0,1,2,7,8,9,10,11,12],control:[2,4,6,9,10,11,13,14],control_const:[11,14],controller_cap:10,controller_const:11,controller_constraint:14,controller_id:[],controllerconstraint:[1,9,14],correspond:[1,9,10,11,14],creat:[9,11,14],cumul:1,current:[10,11],current_bottleneck_first:11,data:[0,1,4,5,6,8,9,11,13,14],defin:[0,11],degre:0,denot:14,destin:[1,4,6,9,10,11],detail:[4,12],determin:10,dict:[1,5,9,10,11,14],dictionari:[1,2,5,9,10,11,13,14],displai:12,divid:[0,11],dst_control:4,dure:4,each:[6,11,14],earliest:11,element:6,enough:11,equal:11,exceed:10,except:13,exist:11,existing_round:11,factor:0,fals:[4,10],file:[6,8,9],find:11,find_scheduling_round:11,first:[6,11,14],fit:11,from:[0,5,9,10,11,14],g:11,gener:[12,14],get:14,get_bottleneck_constraint:11,get_cap:[1,5],get_cap_dict:14,get_capac:0,get_constraint_dict:[1,5,14],get_control:1,get_control_const:[],get_controller_cap_dict:14,get_controller_constraint:9,get_controller_constraint_dict:14,get_controller_id:9,get_controller_idx:1,get_dst_control:4,get_group:[4,5],get_group_id:9,get_group_idx:5,get_load:[0,4],get_load_factor:0,get_migr:9,get_model_bound:8,get_model_data:8,get_qos_const:[],get_qos_constraint:9,get_qos_constraint_dict:14,get_qos_group_cap_dict:14,get_qos_id:[],get_round_id:[],get_switch:[0,1,4,5],get_switch_id:9,get_switch_idx:4,get_total_load:1,given:[1,10],group:[4,5,6,9,10,11,14],group_nam:4,gurobipi:8,ha:[8,11,12],handl:[10,11,14],have:11,heurist:[11,14],hold:0,id:9,identifi:[0,4],implement:11,incur:[0,1,4,6],index:[1,4,5,11,13],indic:[8,10],info:0,inform:[0,1,4,5,10],initi:[8,12],inspir:11,instanc:[2,6,7,8,9,11,12,13,14],instance_data:[8,11,14],instancedata:[8,9,11,14],instancenotspecifi:[8,12],instanti:8,integ:[1,4,5,6,8,9,10,11,14],invalid:12,invalidnam:12,involv:[4,9,11],is_in_group:4,iter:11,its:11,kei:[9,10,11,14],lh:0,linear:8,list:[6,9],load:[0,1,2,4,6,7,8,10,11,12,14],loop:11,lower:8,maintain:11,maximum:[5,6,10,14],member:4,messag:12,method:[0,1,4,5,6,8,9,10],migrat:[0,1,5,7,8,9,11,12,14],migration_fil:[8,9],migrationschedul:[0,1,4,5,6,8,9,10,11,12,14],model:[8,9,10,12,13,14],modelnotoptim:12,modul:[2,7,11,12,13,14],most:11,name:[0,1,4,5,6,9,10,11,12,14],need:[1,5],none:[0,1,4,5,6,8,9,10,11],num_migr:[6,14],num_round:11,number:[5,6,8,10,11,14],object:[1,5,6,8,9,10,11,12,14],obtain:11,one:[8,11,14],optim:[7,12,13],other:11,otherwis:[4,10],output:6,output_fil:6,overload:0,pack:11,page:13,paramet:[0,1,4,5,6,8,9,10,11,12,14],pars:[8,9],parse_migr:9,parser:[7,8,13],part:4,path:8,per:[8,11],perform:4,place:5,pre:8,print:10,print_migr:10,problem:[0,8,10,11],program:8,qo:[2,4,6,9,10,11,13,14],qos_cap:10,qos_const:[11,14],qos_constraint:14,qos_id:[],qosconstraint:[5,9,14],qoscontraint:9,rais:[8,12],reduc:0,reflect:11,rel:11,relat:[4,5,10],remain:[10,11],remov:[0,11],remove_migration_from_constraint:11,remove_switch:0,repres:[0,1,4,5,6,8,9,10,11,12,14],represent:[1,5],respect:[11,14],retriev:[8,14],rh:0,round:[0,1,7,8,11,13,14],round_id:[],round_num:10,run:[6,11],s:[1,11],same:11,schedul:[0,1,5,6,7,8,10,12,14],schedule_migr:10,sdn:4,search:13,second:[6,14],select:11,select_migration_from_constraint:11,set:[0,1,4,5,9,10],should:[4,11],signal:11,signifi:[4,11],simul:[2,13],simultan:5,singl:[0,10,11,14],solut:8,solv:[8,11],sourc:[0,1,4,5,6,8,9,10,11,12,14],specifi:[6,8,9,11,12,14],store:[1,2,4,5,10],str:[0,1,4,5,6,8,9,12],string:[0,1,4,5,6,8,9,10,11,12,14],sum:11,switch_id:[],switch_load:0,switch_nam:[0,1,5],take:[5,8],thi:[0,4,6,11],through:11,to_data:9,total:[0,1],transit:14,tri:12,tupl:6,two:[6,14],uninitializedmodel:12,updat:[9,11],upper:[8,14],upper_bound_round:14,us:[0,1,2,4,6,7,8,9,10,11,14],user:12,util:13,valu:[1,8,9,10,11,14],vector:11,vector_first_fit:11,version:11,we:11,were:0,when:[4,12],whether:10,which:[0,1,4,5,6,11,14],within:[5,14],without:10,work:7,would:0,yet:[8,12]},titles:["Constraint Dictionary","Controller Constraint","Migration Scheduling Data","Instance Data","Switch Migration","QoS Constraint","Migration Simulator","Model","Optimizer","Parser","Migration Round","Scheduling Algorithms","Exceptions","Welcome to Load Migration Scheduling\u2019s documentation!","Utility Functions"],titleterms:{"function":14,"switch":4,algorithm:11,constraint:[0,1,5],control:1,data:[2,3],dictionari:0,document:13,except:12,indic:13,instanc:3,load:13,migrat:[2,4,6,10,13],model:7,optim:8,parser:9,qo:5,round:10,s:13,schedul:[2,11,13],simul:6,tabl:13,util:14,welcom:13}})