clc
clear
close all

NUM_POINTS=2000000;
LEN_SIM=600;
NUM_FAULTS_PER_CHANNEL=1400;
STEP_SIZE=LEN_SIM/NUM_POINTS;
t = 0:STEP_SIZE:LEN_SIM-STEP_SIZE;
% Creating the left wheel sensor data
v_l = ones(1,NUM_POINTS)+(rand(1,NUM_POINTS)*0.1-0.05);
v_l_fault_idx=floor(rand(1,NUM_FAULTS_PER_CHANNEL)*NUM_POINTS);
v_l(v_l_fault_idx)=v_l(v_l_fault_idx)+(rand(1,NUM_FAULTS_PER_CHANNEL)*1.15-0.5);
v_l_fault = zeros(1,NUM_POINTS);
v_l_fault(v_l_fault_idx) = 1;
v_l = v_l * 5;
% pause
% figure
% plot(0:STEP_SIZE:LEN_SIM-STEP_SIZE,v_l);
% pause
v_r = ones(1,NUM_POINTS)+(rand(1,NUM_POINTS)*0.1-0.05);
v_r_fault_idx=floor(rand(1,NUM_FAULTS_PER_CHANNEL)*NUM_POINTS);
v_r(v_r_fault_idx)=v_r(v_r_fault_idx)+(rand(1,NUM_FAULTS_PER_CHANNEL)*1.15-0.5);
v_r_fault = zeros(1,NUM_POINTS);
v_r_fault(v_r_fault_idx) = 1;
v_r = v_r * 5;


v_l_ideal = 5 * ones(1,NUM_POINTS+1);
v_r_ideal = v_l_ideal;

figure
subplot(2,1,1);
plot(0:STEP_SIZE:LEN_SIM-STEP_SIZE , 5*ones(1,NUM_POINTS), 0:STEP_SIZE:LEN_SIM-STEP_SIZE , v_l);
legend('Desired','Noisy signal with faults')
title('Simulated Robot Data - Wheel Velocities');
axis([0 LEN_SIM min(v_l)-1 max(v_l)+1]);
xlabel('Time [s]');
ylabel('w_l [rad/s]');

subplot(2,1,2);
plot(0:STEP_SIZE:LEN_SIM-STEP_SIZE , 5*ones(1,NUM_POINTS) , 0:STEP_SIZE:LEN_SIM-STEP_SIZE , v_r);
legend('Desired','Noisy signal with faults')
axis([0 LEN_SIM min(v_r)-1 max(v_r)+1]);
xlabel('Time [s]');
ylabel('w_r [rad/s]');

figure
pose = zeros(1,NUM_POINTS); 
r = 0.035
d = 0.227
vX = r * (v_r + v_l)/2.0;
w = r * (v_r - v_l) / d;

vX_ideal = r * (v_r_ideal + v_l_ideal)/2.0;
w_ideal = r * (v_r_ideal - v_l_ideal)/d;

x = zeros(1,NUM_POINTS+1);
y = zeros(1,NUM_POINTS+1);
theta = zeros(1,NUM_POINTS+1);

x_ideal = x;
y_ideal = y;
theta_ideal = theta;

x_dot = 0;
y_dot = 0;
for i=1:NUM_POINTS
   x_dot = vX(i) * cos(theta(i));
   y_dot = vX(i) * sin(theta(i));
   theta_dot = w(i);
   

   x(i+1) = x_dot*LEN_SIM/NUM_POINTS + x(i);
   y(i+1) = y_dot*LEN_SIM/NUM_POINTS + y(i);
   theta(i+1) = theta_dot*LEN_SIM/NUM_POINTS  + theta(i);

   x_dot_ideal = vX_ideal(i) * cos(theta_ideal(i));
   y_dot_ideal = vX_ideal(i) * sin(theta_ideal(i));
   theta_dot_ideal = w_ideal(i);
   

   x_ideal(i+1) = x_dot_ideal*LEN_SIM/NUM_POINTS + x_ideal(i);
   y_ideal(i+1) = y_dot_ideal*LEN_SIM/NUM_POINTS + y_ideal(i);
   theta_ideal(i+1) = theta_dot_ideal*LEN_SIM/NUM_POINTS  + theta_ideal(i);

end
subplot(2,1,1)
plot(vX)
plot(0:STEP_SIZE:LEN_SIM,vX_ideal,0:STEP_SIZE:LEN_SIM,[sum(vX)/NUM_POINTS vX])
title('Simulated Robot Data - v_x and \theta');
legend('Desired','Noisy signal with faults')
xlabel('Time [s]');
ylabel('v_x [m/s]');
axis([0 LEN_SIM min(vX)-0.2 max(vX)+0.2]);
subplot(2,1,2)
plot(0:STEP_SIZE:LEN_SIM,theta_ideal,0:STEP_SIZE:LEN_SIM,theta)
legend('Desired','Noisy signal with faults')
axis([0 LEN_SIM min(theta)-0.2 max(theta)+0.2]);
xlabel('Time [s]');
ylabel('\theta [rad]');
% 
% % -------------------------------------------------------------------------
% n=NUM_POINTS;
% Vl=v_l;
% Vr=v_r;
% 
% % distance between the centers of the two wheels
% l=1;
% 
% % calculating R and w for all the values of Vl and Vr
% % R=signed distance from the ICC to the midpoint between the wheels
% % w=rate of rotation
% Rpure=(l/2).*((Vl+Vr)./(Vl-Vr));
% wpure=(Vr-Vl)./l;
% 
% % ICC - Instantaneous Center of Curvature 
% theta=10;
% x_coor=1;
% y_coor=1;
% ICCpure=[x_coor-(Rpure.*sin(theta)), y_coor+(Rpure.*cos(theta))];
% % ICCnoisy=[x_coor-(Rnoisy.*sin(theta)), y_coor+(Rnoisy.*cos(theta))];
% 
% % find new x_coor, new y_coor and new theta (eq 5) pure version
% % figure
% delta_t=1;
% for i=1:n    
% %     sol=[x_coor+(Vr(i)*cos(theta)*delta_t)  y_coor+(Vr(i)*sin(theta)*delta_t)  theta];
%     sol =[cos(wpure(i)*delta_t) -1*sin(wpure(i)*delta_t) 0; sin(wpure(i)*delta_t) cos(wpure(i)*delta_t) 0; 0 0 1]*[x_coor-ICCpure(1); y_coor-ICCpure(2); theta] + [ICCpure(1); ICCpure(2); (wpure(i)*delta_t)];
%     x_coor_dash(i)=sol(1);
%     y_coor_dash(i)=sol(2);
%     theta_dash(i)=sol(3);
% 
%     if i > 1
%        x_coor_dash(i) = x_coor_dash(i) + x_coor_dash(i-1);
%        y_coor_dash(i) = y_coor_dash(i) + y_coor_dash(i-1);
%        theta_dash(i) = theta_dash(i) + theta_dash(i-1);
%     end
% 
%     version1(i)=1;
% %     plot(x_coor_dash(i),y_coor_dash(i))
% %     hold on
% end
% 
% % pose_actual = zeros(1,NUM_POINTS);% TODO: Populate with your equations using v_l and v_r as inputs
% % pose_actual=x_coor_dash;
% % -------------------------------------------------------------------------
% 
% ind1=find(x_coor_dash>(3*mean(x_coor_dash)));
% ind2=find(x_coor_dash<(-3*mean(x_coor_dash)));
% xaxis=0:STEP_SIZE:LEN_SIM-STEP_SIZE;
% 
x_desired = zeros(1,NUM_POINTS+1)
y_desired = 0:STEP_SIZE:LEN_SIM;
figure
hold on
% subplot(3,1,3);
plot(x_ideal,y_ideal,x,y);% , pose , xaxis , x_coor_dash);

% for i=1:length(ind1)
%     plot(xaxis(ind1(i)),x_coor_dash(ind1(i)),'ro')
%     hold on
% end
% % pause
% for i=1:length(ind2)
%     plot(xaxis(ind2(i)),x_coor_dash(ind2(i)),'ro')
%     hold on
% end
legend('Desired', 'Noisy pose with faults')
% axis square;
xlabel('x [m]');
ylabel('y [m]');
title('Simulated Robot Data - Cartesian Pose');
axis([0 max(x)+0.1 -0.5 0.5])
%axis([floor(min(x)-min(x)*0.1) max(x)+0.1*max(x) floor(-1*max(abs(y))-0.1*max(abs(y))) max(abs(y))+0.1*max(abs(y))])

% figure
% subplot(4,1,4);
% plot(0:STEP_SIZE:LEN_SIM-STEP_SIZE , pose , 0:STEP_SIZE:LEN_SIM-STEP_SIZE , y_coor_dash);
% legend('Desired', 'Noisy pose with faults')
% % axis square;
% xlabel('x [m]');
% ylabel('y [m]');
% title('Robot Pose')
csvwrite('/tmp/time.csv',t)
csvwrite('/tmp/vleft.csv',v_l)
csvwrite('/tmp/vright.csv',v_r)
csvwrite('/tmp/vx.csv',vX)
csvwrite('/tmp/vw.csv',w)
csvwrite('/tmp/vleft_faultlabel.csv',v_l_fault)
csvwrite('/tmp/vright_faultlabel.csv',v_r_fault)
csvwrite('/tmp/y.csv',y)
csvwrite('/tmp/x.csv',x)
csvwrite('/tmp/x_desired.csv',x_desired)
csvwrite('/tmp/y_desired.csv',y_desired)
csvwrite('/tmp/vx_desired.csv',vX_ideal)
csvwrite('/tmp/w_desired.csv',w_ideal)
datafilecmd=sprintf('tar -czvf data-%s.tar.gz /tmp/*.csv',strrep(strrep(datestr(datetime('now')),' ','-'),':','-'))
system(datafilecmd)
