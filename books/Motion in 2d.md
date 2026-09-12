# 4. MOTION IN A PLANE

## 1. INTRODUCTION

Motion in a plane is a two dimensional motion. The analysis of this type of motion becomes easy when we treat this motion as a combination of two straight line motions along two mutually perpendicular axes lying in the plane of motion. In Cartesian coordinate system the two mutually perpendicular axes are the x-axis and the y-axis respectively. The displacement, velocity and acceleration of the particle are resolved into components along the x and y axes and motion along each axis is studied independent of the other. The net displacement, velocity and acceleration is the vector sum of their respective components along the two axes. In this chapter we will discuss about the motion of a projectile, the motion of a body relative to another body, the motion of a body in a medium, motion of an airplane with respect to wind, and circular motion.

## 2. MOTION IN A PLANE

When a body moves in a straight line, we call it motion in a straight line or one dimension. For eg, a car moving straight on a road. When you throw a ball towards your friend, the ball follows a non-linear path. This motion is termed as motion in two dimensions or motion in a plane.

The position of a particle that is free to move can be located by two coordinates in a plane. We choose the plane of motion as the X-Y plane. We choose a suitable instant as $t = 0$ and choose the origin at the place where the particle is situated at $t = 0$. Any two convenient mutually perpendicular directions in the X-Y plane are chosen as the X and Y-axes.

## 3. PROJECTILE MOTION

Projectile motion is a form of motion in which an object or particle (here called a projectile) is thrown in a given direction near the earth's surface, and it moves along a curved path under the action of a continuous force. The path observed during a projectile motion is called its trajectory. Projectile motion is possible only when there is one force applied at the beginning of the trajectory, after which there is no force in operation except gravity.

### 3.1 Ground-To-Ground Projectile

In the Fig. 3.2 shown, let us consider the horizontal surface through the point O. Now, the point O here is called the point of projection, the angle $\theta$ is called the angle of projection and the distance OB is called the horizontal range or simply range. Further, the total time taken by the particle in describing the path OAB is called the time of flight.

However, we can separately discuss the motion of the projectile for both the horizontal and vertical parts. In this regard, we begin by considering the origin as the point of projection.

Now, we have 
$$u_x = u\cos\theta; \quad a_x = 0; \quad u_y = u\sin\theta; \quad a_y = -g.$$

### 3.1.1 Horizontal Motion

As $a_x = 0$, we have 
$$v_x = u_x + a_x t = u_x = u\cos\theta \quad \text{and} \quad x = u_x t + \frac{1}{2}a_x t^2 = u_x t = ut\cos\theta$$

### 3.1.2 Vertical Motion

In the downward direction, we know that the acceleration of the particle is g. Thus, $a_y = -g$.
Further, the y-component of the initial velocity is $u_y$. Thus,
$$v_y = u_y - gt \quad \text{and} \quad y = u_y t - \frac{1}{2}gt^2; \quad \text{also we have, } v_y^2 = u_y^2 - 2gy.$$

### 3.1.3 Time of Flight

Let us suppose that the particle is at B at time t. Therefore, the equation for horizontal motion gives $OB = x = ut\cos\theta$.
However, the y-coordinate at the point B is zero. Thus, from the equation of vertical motion,
$$y = ut\sin\theta - \frac{1}{2}gt^2 \quad \text{or, } \quad 0 = ut\sin\theta - \frac{1}{2}gt^2 \quad \text{or, } \quad t\left(u\sin\theta - \frac{1}{2}gt\right) = 0$$
Thus, either $t = 0 \text{ or } t = \frac{2u\sin\theta}{g}$

Now, $t = 0$ exactly corresponds to the initial position O of the particle. Hence, the time at which it reaches B is the time of flight.
$$T = \frac{2u\sin\theta}{g}$$
This equation helps us to exactly calculate the time of flight.

### 3.1.4 Range

Consider the distance OB covered by a particle, which is the horizontal range. It is the distance travelled by the particle in time $T = \frac{2u\sin\theta}{g}$
By the equation of horizontal motion, 
$$x = (u\cos\theta) \times T \quad \text{or, } \quad OB = \frac{2u^2 \sin\theta \cos\theta}{g} = \frac{u^2 \sin 2\theta}{g}$$

### 3.1.5 Maximum Height

We have, $v_y = u_y - gt = u\sin\theta - gt$
However, at the maximum height, 
$$0 = u\sin\theta - gt \quad \text{or, } \quad t = \frac{u\sin\theta}{g}$$
The actual maximum height is 
$$H = u_y t - \frac{1}{2}gt^2 = (u\sin\theta)\left(\frac{u\sin\theta}{g}\right) - \frac{1}{2}g\left(\frac{u\sin\theta}{g}\right)^2$$
$$= \frac{u^2 \sin^2\theta}{g} - \frac{1}{2}\frac{u^2 \sin^2\theta}{g} = \frac{u^2 \sin^2\theta}{2g}$$

## EQUATION OF TRAJECTORY OF A PROJECTILE

$$x = (u\cos\alpha)t \quad \therefore t = \frac{x}{u\cos\alpha}$$
By substituting this value of t in $y = (u\sin\alpha)t - \frac{1}{2}gt^2$, we obtain
$$y = x\tan\alpha - \frac{gx^2}{2u^2 \cos^2\alpha} = x\tan\alpha - \frac{gx^2}{2u^2}\sec^2\alpha = x\tan\alpha - \frac{gx^2}{2u^2}(1 + \tan^2\alpha)$$
The above are the standard equations of trajectory of any projectile. Here, we should be aware of the fact that the equation is quadratic in x. This is why the path of a projectile is always a parabola. Further, the above equation can also be represented in terms of range (R) of the projectile as 
$$y = x\left(1 - \frac{x}{R}\right)\tan\alpha$$

**Illustration 1:** Assume that a ball is thrown from a field at a speed of 12.0 m/s and at an angle of 45° with the horizontal. At what distance will it hit the field again? Take $g = 10.0 \text{ m/s}^2$. **(JEE MAIN)**

**Sol:** Use the formula for the range of a projectile.
$$\text{The horizontal range } = \frac{u^2 \sin 2\theta}{g} = \frac{(12 \text{ m/s})^2 \times \sin(2 \times 45^\circ)}{10 \text{ m/s}^2} = \frac{144 \text{ m}^2/\text{s}^2}{10.0 \text{ m/s}^2} = 14.4 \text{ m}$$
Thus, the ball hits the field exactly at 14.4 m from the point of projection.

*(Handwritten note: $u=12$, $\theta=45^\circ$, $g=10$, $\frac{u^2 \sin 2\theta}{g} = \frac{12 \times 12 \times 1}{10} = \frac{72}{5} = 14.4$)*

---
**CONCEPTS**
(i) Range is maximum where $\sin 2\alpha = 1$ or $\alpha = 45^\circ$ and this maximum range is:
$$R_{\text{max}} = \frac{u^2}{g} = 4H$$
(ii) For given value of u, range at $\alpha$ and range at $\phi$ are equal although times of flight and maximum heights may be different. Because
$$R_{90^\circ - \alpha} = \frac{u^2 \sin 2(90^\circ - \alpha)}{g} = \frac{u^2 \sin(180^\circ - 2\alpha)}{g} = \frac{u^2 \sin 2\alpha}{g} = R_\alpha$$
As we have seen in the above derivations that $a_x = 0$, i.e., motion of the projectile in the horizontal direction is uniform. Hence, horizontal component of velocity $u\cos\alpha$ does not change during its motion.
Motion in the vertical direction is first retarded and then accelerated in opposite direction. As the equation of trajectory of projectile is of the form, $y = ax - bx^2$ (equation of parabola), therefore, the path followed by a projectile is a parabola.
**B Rajiv Reddy (JEE 2012, AIR 11)**

---

**Illustration 2:** Find the angle of a projectile for which both the horizontal range and maximum height are equal. **(JEE MAIN)**

**Sol:** Use the formula for the range and maximum height of a projectile.
Given, $R = H$
$$\therefore \frac{u^2 \sin 2\alpha}{g} = \frac{u^2 \sin^2 \alpha}{2g} \quad \text{or} \quad 2\sin\alpha \cos\alpha = \frac{\sin^2 \alpha}{2} \quad \text{or} \quad \frac{\sin\alpha}{\cos\alpha} = 4 \quad \text{or} \quad \tan\alpha = 4 \quad \alpha = \tan^{-1}(4)$$
*(Handwritten note: $\frac{u^2 \sin 2\theta}{g} = \frac{u^2 \sin^2 \theta}{2g} \implies 2 u^2 \sin 2\theta = u^2 \sin^2 \theta \implies 2 \sin\theta \cos\theta = \frac{\sin^2 \theta}{2} \implies 4 = \tan\theta \implies \theta = \tan^{-1}(4)$)*

**Illustration 3:** The given Fig. 3.4 shows a pirate ship 560 m from a fort defending a harbor entrance. A defense canon, located at sea level, fires balls at initial speed $v_0 = 82\text{ m/s}$. **(JEE ADVANCED)**

(a) At what angle $\theta_0$ from the horizontal must a ball be fired to hit the ship?

**Sol:** Use the formula for the range of a projectile to find the angle of projection.
We can relate the launch angle $\theta_0$ to the range R with Eq. ($R = (v_0^2/g)\sin 2\theta_0$), which, after rearrangement, gives
$$\theta_0 = \frac{1}{2} \sin^{-1} \frac{gR}{v_0^2} = \frac{1}{2} \sin^{-1} \frac{(9.8 \text{ m/s}^2)(560 \text{ m})}{(82 \text{ m/s})^2} = \frac{1}{2} \sin^{-1} 0.816$$
One solution of (54.7°) is worked out using a calculator; now, we subtract it from 180° to get the other solution (125.3°). This gives us $\theta_0 = 27^\circ$ and $\theta_0 = 63^\circ$.
*(Handwritten note: $\frac{u^2 \sin 2\theta}{g} = R \implies \theta = \frac{1}{2} \sin^{-1} \left( \frac{gR}{u^2} \right) = \frac{9.8 \times 560}{82 \times 82}$)*

**Illustration 4:** Suppose a batsman B hits a high-fly ball to the outfield, directly toward an outfielder F and with a launch speed of $v_0 = 40 \text{ m/s}$ and a launch angle of $\theta_0 = 35^\circ$. During the flight, a line from the outfielder to the ball makes an angle $\phi$ with the ground. Based on the data provided, plot the elevation angle $\phi$ versus t, assuming that the outfielder is (a) already positioned to catch the ball, (b) is 6.0 m too close to the batsman, and (c) is 6.0 m too far away. **(JEE ADVANCED)**

**Sol:** While trying to catch a ball which has gone to a great height you can imagine that the angle of line of sight increases as the ball moves. If we neglect air drag, then the ball is a projectile for which the vertical motion and the horizontal motion can be analyzed individually.

Assuming that the ball is caught at approximately the height it is hit, the horizontal distance traveled by the ball is the range R, given by Eq. ($R = (v_0^2/g)\sin 2\theta_0$)
The ball can be caught if the outfielder's distance from the batsman equals the range R of the ball. Using the above equation, we find the elevation angle $\phi$ for a ball that was hit toward an outfielder is (a) defined and (b) plotted versus time t.
$$R = \frac{v_0^2}{g} \sin 2\theta_0 = \frac{(40 \text{ m/s})^2}{9.8 \text{ m/s}^2} \sin(70^\circ) = 153.42 \text{ m}$$
Fig. 3.5 (a) above shows a snapshot of the ball in flight when the ball is at height y and horizontal distance x from the batsman (who is at the origin). The horizontal distance of the ball from the outfielder is R - x, and the elevation angle $\phi$ of the ball in the outfielder's view is given by $\tan\phi = y / (R - x)$.
Thus, using $v_0 = 40 \text{ m/s}$ and $\theta_0 = 35^\circ$, we have 
$$\phi = \tan^{-1} \frac{(40 \sin 35^\circ)t - 4.9 t^2}{153.42 - (40 \cos 35^\circ)t}$$
By graphing this function versus t gives us the middle plot in b. We now see that the ball's angle in the outfielder's view increases at an almost steady rate throughout the flight.
If the outfielder is 6.0 m close to the batsman, then we replace the distance of 153.42 m in the given equation with $153.42 \text{ m} - 6.0 \text{ m} = 147.42 \text{ m}$. Further, regraphing the function gives the "Too close" plot as in Fig. 3.5 (b).
Now, we observe that the elevation angle of the ball rapidly increases toward the end of the flight as the ball soars over the outfielder's head. However, if the outfielder is 6.0 m too far away from the batsman then we replace the distance of 153.42 m in the equation with $159.42 \text{ m}$. The resulting plot is hence labeled "Too far" in the Fig. 3.5 (b), angle first increases and thereafter rapidly decreases.
Conclude: Thus, if a ball is hit directly toward an outfielder, then the player can tell from the change in the ball's elevation angle $\phi$ whether to stay put, run toward the batter, or back away from the batsman.

**Illustration 5:** Suppose that a projectile is fired horizontally with a velocity of 98 m/s from the top of a hill that is 490 m high. Find:
*(Handwritten note: $u_x = 98\text{m/s}$)*
(a) The time taken by the projectile to reach the ground,
(b) The distance of the point where the particle hits the ground from the foot of the hill and
(c) The velocity with which the projectile hits the ground. (take $g = 9.8 \text{ m/s}^2$) **(JEE MAIN)**

**Sol:** Let x-axis be along the horizontal and the y-axis be along the vertical. The projectile will have uniform velocity along the positive x-axis and uniform acceleration along the negative y-axis.

In this problem, we cannot apply the formulae of R, H and T directly. Necessarily we have to follow the three steps discussed in the theory. Here, however, it will be more convenient to choose x and y directions as shown in the Fig. 3.6 provided.

Here, $u_x = 98 \text{ m/s}, a_x = 0, u_y = 0$ and $a_y = g$

(a) At A, $S_y = 490\text{m}$. Therefore, applying $S_y = u_y t + \frac{1}{2}a_y t^2$
$\therefore 490 = 0 + \frac{1}{2}(9.8)t^2 \quad \therefore t = 10\text{s}$

(b) $BA = s_x = u_x t + \frac{1}{2}a_x t^2 \quad \text{or} \quad BA = (98)(10) + 0 \quad \text{or} \quad BA = 980\text{m}$

(c) $v_x = u_x = 980\text{m/s}$; $\quad v_y = u_y + a_y t = 0 + (9.8)(10) = 98\text{m/s}$
$\therefore v = \sqrt{v_x^2 + v_y^2} = \sqrt{(98)^2 + (98)^2} = 98\sqrt{2}\text{ m/s}$

and $\tan\beta = \frac{v_y}{v_x} = \frac{98}{98} = 1 \quad \therefore \beta = 45^\circ$

Thus, we show that the projectile hits the ground with a velocity $98\sqrt{2}\text{ m/s}$ at an angle of $\beta = 45^\circ$ with horizontal as shown in the Fig. 3.6 provided.

---

### 6. RELATIVE MOTION

The measurements describing motion are generally subject to the state of motion of the frame of reference with respect to which measurements are taken about. Our day-to-day perception of motion is generally based on our earth's view — a view common to all bodies at rest with respect to earth. However, we come across cases when there is a subtle perceptible change in our view of earth. One such case is traveling in the city trains. We easily find that it takes lot longer to overtake another train on a parallel track. Also, we happen to see two people talking while driving separate cars in parallel lanes, as if they were stationary to each other! In terms of kinematics, as a matter of fact, they are actually stationary to each other even though each of them is in motion with respect to ground.

In this topic, we study motion from a perspective other than that of our earth. The only condition that we subject ourselves is that two references or two observers making the measurements of motion of an object, are moving at constant velocity.

We now consider two moving observers, 'A' and 'B':
The relative velocity of A with respect of B (written as $v_{AB}$) is $\bar{v}_{AB} = \bar{v}_A - \bar{v}_B$
Similarly, the relative acceleration of A with respect to B is $\bar{a}_{AB} = \bar{a}_A - \bar{a}_B$

**Illustration 9:** Assume that two cars, standing apart, start moving toward each other at speeds of $1\text{ m/s}$ and $2\text{ m/s}$ along a straight road. What could be the speed with which they approach each other?
**(JEE MAIN)**

**Sol:** Let us consider that "A" denotes earth, "B" denotes the first car and "C" denotes the second car. Therefore, the equation of relative velocity for this case is: $v_{BA} = 1\text{m/s}$ and $v_{CA} = -2\text{m/s}$.
$v_{CA} = v_{BA} + v_{CB} \implies -2 = 1 + v_{CB} \implies v_{CB} = -2 - 1 = -3\text{m/s}$
This implies that the car "C" is approaching "B" at a speed of $-3\text{m/s}$ along the straight road. Further, it also means that the car "B" is approaching "C" at a speed of $3\text{ m/s}$ along the straight road. We, therefore, say that the two cars approach each other at relative speed of $3\text{ m/s}$.

To evaluate relative velocity, we proceed as follows:
* Apply velocity of the reference object (say object "A") to other object(s) and hence render the reference object at rest.
* The resultant velocity of the other object ("B") is therefore equal to relative velocity of "B" with respect to "A".

**CONCEPTS**
* The foremost thing in solving problems of relative motion is about visualizing measurement. If we say a body "A" has relative velocity "v" with respect to another moving body "B", then we simply mean that we are making measurement from the moving frame (reference) of "B".
* It is helpful in solving problem to make reference object stationary by applying negative of its velocity to both objects. The resultant velocity of the moving object is equal to the relative velocity of the moving object with respect to reference object. If we interpret relative velocity in this manner, it gives easy visualization as we are accustomed to observing motion from stationary state.

**Nitin Chandrol (JEE 2012, AIR 134)**

**Illustration 10:** Assume that a boy is riding a cycle at a speed of $5\sqrt{3}\text{ m/s}$ toward east along a straight line. It is raining at a speed of $15\text{ m/s}$ in the vertical direction. What is the direction of rainfall as observed by the boy?
**(JEE MAIN)**

**Sol:** Let us denote earth, boy and rain with symbols A, B and C, respectively.
The question here provides the velocity of B and C with respect to A (earth).
$v_{BA} = 5\sqrt{3}\text{ m/s}$; $\quad v_{CA} = 15\text{ m/s}$

Now, we need to determine the direction of rain (C) with respect to boy (B),
i.e., $v_{CB}$. $\quad v_{CA} = v_{BA} + v_{CB} \implies v_{CB} = v_{CA} - v_{BA}$

Thus, we now draw the vector diagram to evaluate the terms on the right side of the equation. Therefore, here, we need to evaluate "$v_{CA} - v_{BA}$", which is equivalent to "$v_{CA} + (-v_{BA})$". We now apply parallelogram theorem to obtain vector sum as represented in the Fig. 3.14 provided.

For the boy (B), the rain appears to fall, making an angle "$\theta$" with the vertical ($-y$ direction).
$\implies \tan\theta = \frac{v_{BA}}{v_{CA}} = \frac{5\sqrt{3}}{15} = \frac{1}{\sqrt{3}} = \tan30^\circ \implies \theta = 30^\circ$

**Illustration 11:** Consider that a person is driving a car toward east at a speed of $80\text{ km/hr}$. A train appears to move toward north with a velocity of $80\sqrt{3}\text{ km/hr}$ to this person. Find the speed of the train as measured with respect to earth.
**(JEE ADVANCED)**

**Sol:** The velocity of the train with respect to earth is the vector sum of its velocity with respect to car and velocity of car with respect to earth.
Let us first denote the car and train as "A" and "B", respectively. Here, we are provided with the speed of car ("A") with respect to earth, i.e., "$v_A$" and speed of train ("B") with respect to "A",
i.e., $v_{BA}$. $\quad v_A = 80\text{km/hr}$; $v_{BA} = 80\sqrt{3}\text{km/hr}$
Now, we are required to find the speed of train ("B") with respect to earth, i.e., $v_B$. From the equation of relative motion, we have
$$v_{BA} = v_B - v_A \implies v_B = v_{BA} + v_A$$

---

To evaluate the right-hand side of the equation, we draw vectors "$v_{BA}$" and "$v_A$" and use parallelogram law to find the actual speed of the train.

$\implies v_B = \sqrt{(v_{BA})^2 + (v_A)^2} = \sqrt{\left(80\sqrt{3}\right)^2 + 80^2} = 160\text{km/hr}$

### 6.1 Motion of Boat in a Stream

In this section, we consider a general situation of sailing of a boat in a moving stream of water. However, in order to keep our context simplified, we consider that the stream is unidirectional in x-direction and the width of stream, "d", is constant. Let the velocities of boat (A) and stream (B) be "$v_A$" and "$v_B$", respectively with respect to ground. The velocity of boat (A) with respect to stream (B), therefore, is

$v_{AB} = v_A - v_B \implies v_A = v_{AB} + v_B$

We represent these velocities in the Fig. 3.16 provided. It is clear from the Fig. 3.16 provided that boat sails in the direction, making an angle "$\theta$" with y-direction, but reaches destination in different direction. The boat obviously is carried along the stream in x-direction. This displacement in x-direction (x = QR) from the directly opposite position to actual position on the other side of the stream is called the drift of the boat.

#### 6.1.1 Resultant Velocity
We can calculate the magnitude of resultant velocity using the parallelogram theorem,

$v_A = \sqrt{v_{AB}^2 + v_B^2 + 2v_{AB}v_B\cos\alpha}$

where "$\alpha$" is the angle between $v_B$ and $v_{AB}$ vectors. The angle "$\beta$" formed by the resultant velocity with x-direction is given as: $\tan\beta = \frac{v_{AB}\sin\alpha}{v_B + v_{AB}\cos\alpha}$

#### 6.1.2 Time to Cross the Stream
The boat covers a final distance equal to the width of stream "d" in the time "t" in y-direction. Now, by applying the concept of independence of motions in perpendicular directions, we can say that boat covers a final distance "OQ = d" with a speed equal to the component of resultant velocity in y-direction.

Now, the resultant velocity is composed of (i) velocity of boat with respect to stream and (ii) velocity of stream. Here, we observe that velocity of stream is perpendicular to y-direction. Therefore, it does not have any component in y-direction. We, therefore, conclude that the component of the resultant velocity is equal to the component of the velocity of boat with respect to stream in y-direction. Note that the two equal components shown in the Fig. 3.17 provided are geometrically equal as they are altitudes of same parallelogram. Hence, $v_{Ay} = v_{ABy} = v_{AB}\cos\theta$
where "$\theta$" is the angle that relative velocity of boat w.r.t stream makes with the vertical. $\quad t = \frac{d}{v_{Ay}} = \frac{d}{v_{AB}\cos\theta}$

Thus, we can use either of these two expressions to calculate time to cross the river, depending on the inputs available.

#### 6.1.3 Drift of the Boat
We now know that the displacement of the boat in x-direction is independent of motion in the perpendicular direction. Hence, displacement in x-direction is achieved with the component of resultant velocity in x-direction.
$$x = (v_{Ax})t = (v_B - v_{ABx})t = (v_B - v_{AB}\sin\theta)t$$

Then, substituting for time "t", we have: $\quad x = (v_B - v_{AB}\sin\theta)\frac{d}{v_{AB}\cos\theta}$

#### 6.1.4 Shortest Interval to Cross the Stream

The time taken by the boat to cross the river is given by: $t = \frac{d}{v_{Ay}} = \frac{d}{v_{AB}\cos\theta}$
Clearly, the time taken is minimum for the greatest value of denominator. The denominator is maximum for $\cos\theta = 1$
for this value, $\quad t_{\min} = \frac{d}{v_{AB}}$
This means that the boat needs to sail in the direction perpendicular to the stream to reach the opposite side in minimum time. The drift of the boat for this condition is: $x = \frac{v_Bd}{v_{AB}}$

**CONCEPTS**
We have discussed motion with specific reference to boat in a water stream. However, the consideration is general and is applicable to the motion of a body in a medium. For example, the discussion and analysis can be extended to the motion of an aircraft, whose velocity is modified by the motion of the wind.
**GV Abhinav (JEE 2012, AIR 329)**

**Illustration 12:** An aircraft flies with velocity of $200 (\sqrt{2}) \text{km/hr}$ and the wind is blowing from the south. If the relative velocity of the aircraft with respect to wind is $1000\text{ km/hr}$, then find the direction in which the aircraft should fly such that it reaches a destination in the north-east direction.
**(JEE MAIN)**

**Sol:** The vector sum of the velocity of the airplane with respect to the wind and the velocity of the wind with respect to ground is equal to velocity of the aircraft with respect to ground. This net velocity should be in north-east direction.

We show the velocities pertaining to this problem in the Fig. 3.18 provided. In the Fig. 3.18 provided, OP denotes the velocity of the aircraft in still air or equivalently it represents the relative velocity of the aircraft with respect to air in motion; PQ denotes the velocity of the wind and OQ denotes the resultant velocity of the aircraft. However, it is clear that the aircraft should fly in the direction OP so that it is ultimately led to follow the north-east direction.

We should understand here that one of the velocities is the resultant velocity of the remaining two velocities. Therefore, it follows that the three velocity vectors are represented by the sides of a closed triangle.

We can now demonstrate the direction of OP, if we can find the angle "$\theta$". The easiest way to determine the angle between vectors composing a triangle is to apply the sine law,

$$\frac{OP}{\sin 45^\circ} = \frac{PQ}{\sin\theta}$$

Therefore, by substituting these values, we obtain

---

$$\sin\theta = \frac{PQ\sin45^\circ}{OP} = \frac{200\sqrt{2}}{1000 \times \sqrt{2}} = \frac{1}{5} = 0.2$$
$$\theta = \sin^{-1}(0.2)$$
Hence, based on the above analysis, the aircraft should steer in the direction, making an angle with east as given by: $\theta' = 45^\circ - \sin^{-1}(0.2)$

**Illustration 13:** Assume that a boat, capable of sailing at $2\text{ m/s}$, moves upstream in a river. The water in the stream flows at $1\text{ m/s}$. A person walks from the front to the rear end of the boat at a speed of $1\text{ m/s}$ along the liner direction. What is the speed of the person (m/s) with respect to the ground?
**(JEE MAIN)**

**Sol:** First find the velocity of boat with respect to ground. The velocity of man with respect to boat is added to the velocity of boat with respect to ground to get the velocity of man with respect to ground.

Let us assume that the direction of stream be in x-direction and the direction across stream be in y-direction. We further denote boat with "A", stream with "B", and the person with "C". We can now solve this problem in two parts. In the first part, we find out the velocity of boat (A) with respect to ground and then we calculate the velocity of the person (C) with respect to ground.

Here,
velocity of boat (A) with respect to stream (B): $v_{BA} = -2\text{ m/s}$
Velocity of the stream (A) with respect to ground: $v_B = 1\text{ m/s}$
Velocity of the person (C) with respect to boat (A): $v_{CA} = 1\text{ m/s}$
Velocity of the person (C) with respect to ground: $v_C = ?$

The velocity of boat with respect to ground is equal to the resultant velocity of the boat as given by: $v_A = v_{BA} + v_B \implies v_A = -2 + 1 = -1\text{m/s}$

For the motion of person and boat, the velocity of the person with respect to ground is equal to the resultant velocity of (i) velocity of the person (C) with respect to boat (A) and (ii) velocity of the boat (A) with respect to ground. Hence, $v_C = v_{CA} + v_A \implies v_C = 1 + (-1) = 0$.

**Rain problem:** In these type of problems, we again come across three terms $\vec{v}_r, \vec{v}_m \text{ and } \vec{v}_{rm}$. Here
$\vec{v}_r$ = velocity of rain
$\vec{v}_m$ = velocity of man (it may be velocity of cyclist or velocity of motorist also)
and $\vec{v}_{rm}$ = velocity of rain with respect to man
Here, $\vec{v}_{rm}$ is the velocity of rain which appears to the man. Now, let us take one example of this

**Illustration 14:** Rain appears to fall vertically to a man walking at a rate of $3\text{km/h}$. At a speed of $6\text{ km/h}$, it appears to meet him at an angle of $45^\circ$ of vertical. Find out the speed of rain.
**(JEE MAIN)**

**Sol:** This problem is best solved by using Cartesian coordinates. Take x-axis along the horizontal and y-axis vertically upwards. The velocity of man is along positive x-axis. The velocity of rain has both horizontal and vertical components. Express the velocity of man and rain in terms of unit vectors $\hat{i}$ and $\hat{j}$.
Let

$\hat{i}$ and $\hat{j}$ be the unit vectors in horizontal and vertical directions, respectively.
Velocity of rain
$\vec{v}_r = a\hat{i} + b\hat{j}$
Then the speed of rain will be
$|\vec{v}_r| = \sqrt{a^2 + b^2}$

In the first case, $\vec{v}_m = \text{velocity of man} = 3\hat{i}$
$\therefore \vec{v}_{rm} = \vec{v}_r - \vec{v}_m = (a-3)\hat{i} + b\hat{j}$ It seems to be in vertical direction. Hence, $a - 3 = 0$ or $a = 3$

In the second case $\vec{v}_m = 6\hat{i}$
$\therefore \vec{v}_{rm} = (a-6)\hat{i} + b\hat{j} = -3\hat{i} + b\hat{j}$
This seems to be at $45^\circ$ of vertical. Hence, $|b| = 3$

Therefore, from Eq. (ii) speed of rain is $|\vec{v}_r| = \sqrt{3^2 + 3^2} = 3\sqrt{2} \text{ km/h}$

**Alternative Solution:**
[Diagram showing vectors and triangles for Alternative Solution]
combining these two we get
$|\vec{v}_r| = 3\sqrt{2}$

**7. CIRCULAR MOTION**
**Circular motion** is a movement of an object/particle along the circumference of a circle or motion along a circular path. However, it can be uniform or non uniform.

Familiar examples of circular motion include an artificial satellite orbiting the earth at constant height, a stone which is tied to a rope and is being swung in circles and a car turning through a curve in a race track.

**Angular displacement** of a body is the angle in radians (degrees, revolutions) through which a point or line has been turned in a specified sense about a specified axis. Angular displacement is denoted by $\theta$.

**The angular velocity** is defined as the rate of change of angular displacement. The SI unit of angular velocity is radians per second. Angular velocity is usually represented by the symbol omega ($\omega$). $\omega = \frac{d\theta}{dt} = \frac{v}{r}$ where $v$ is linear velocity.

**Angular acceleration** is the rate of change of angular velocity. In SI units, it is measured in radians per second squared ($\text{rad/s}^2$), and is usually denoted by the Greek letter alpha ($\alpha$).
$\alpha = \frac{d\omega}{dt} = \frac{d^2\theta}{dt^2}$, or $\alpha = \frac{a_t}{r}$

---

**7.1 Uniform Circular Motion**
**Uniform Circular Motion**, involves continuous change in the direction of velocity without any change in its magnitude ($v$). A change in the direction of velocity is a change in velocity ($\mathbf{v}$). This implies that UCM is associated with acceleration and hence force. Thus, UCM signifies “presence” of force.

In other words, UCM requires a force, which is always perpendicular to the direction of velocity. Since the direction of velocity is continuously changing, the direction of force, being perpendicular to velocity, should also change continuously.

The direction of velocity along the circular trajectory is always tangential in nature. The perpendicular direction to the circular trajectory is, therefore, known as the radial direction. It implies that force (and hence acceleration) in uniform circular motion is radial. For this reason, acceleration in UCM is recognized to require center, i.e., centripetal (seeking center).

Irrespective of whether circular motion is uniform (constant speed) or non-uniform (varying speed), the circular motion inherently associates a radial acceleration to ensure that the direction of motion is continuously changed—at all instants. We learn about the magnitude of radial acceleration soon, but let us be emphatic to differentiate radial acceleration (accounting change in direction that arises from radial force) with tangential acceleration (accounting change in the speed that arises from tangential force).

The coordinates of the particle is given by the x- and y-coordinate pair as: $x = r\cos\theta$; $y = r\sin\theta$
The angle “$\theta$” is measured anti-clockwise from the x-axis.

The position vector of the position of the particle, $\mathbf{r}$, is represented in terms of unit vectors as:
$\mathbf{r} = x\hat{i} + y\hat{j} \Rightarrow \mathbf{r} = r\cos\theta \hat{i} + r\sin\theta \hat{j} \Rightarrow \mathbf{r} = r(\cos\theta \hat{i} + \sin\theta \hat{j})$

The magnitude of velocity of the particle ($v$) is constant by the definition of UCM. In component form, however, the velocity (refer to the Fig. 3.21) is:
$\mathbf{v} = v_x \hat{i} + v_y \hat{j}$; $v_x = -v\sin\theta$; $v_y = v\cos\theta$
$\sin\theta = \frac{y}{r}$; $\cos\theta = \frac{x}{r}$; $\mathbf{v} = -v\frac{y}{r} \hat{i} + v\frac{x}{r} \hat{j}$

Acceleration: Knowing that speed, “$v$” and radius of circle, “$r$” are constants, we easily differentiate the expression of velocity with respect to time to obtain expression for centripetal acceleration as:
$\mathbf{a} = -\frac{v}{r}\left(\frac{dy}{dt}\hat{i} - \frac{dx}{dt}\hat{j}\right) \Rightarrow \mathbf{a} = -\frac{v}{r}(v_y \hat{i} - v_x \hat{j})$

Substituting the value of component velocities in terms of angle, we obtain
$\Rightarrow \mathbf{a} = -\frac{v}{r}(v\cos\theta \hat{i} - v\sin\theta \hat{j}) = a_x \hat{i} + a_y \hat{j}$        where $a_x = -\frac{v^2}{r}\cos\theta$; $a_y = -\frac{v^2}{r}\sin\theta$

It is evident from the equation of acceleration that it varies as the angle with horizontal, “$\theta$” change. Therefore, the magnitude of acceleration is
$a = |\mathbf{a}| = \sqrt{\left(a_x^2 + a_y^2\right)} \Rightarrow a = |\mathbf{a}| = \frac{v}{r}\sqrt{\left\{v^2 \left(\cos^2 \theta + \sin^2 \theta\right)\right\}} \Rightarrow a = \frac{v^2}{r}$

**Illustration 14:** Assume that a cyclist negotiates the curvature of 20 m at a speed of 20 m/s. What is the magnitude of his acceleration? (JEE MAIN)
**Sol:** The speed of the cyclist moving along circular path is constant. So its acceleration is centripetal.
Let the speed of the cyclist be constant. Then, the acceleration of the cyclist is the centripetal acceleration that is required to move the cyclist along a circular path, i.e., the acceleration resulting from the change in the direction of motion along the circular path.

Hence, $v = 20\text{ m/s}$ and $r = 20\text{ m} \Rightarrow a = \frac{v^2}{r} = \frac{20^2}{20} = 20\text{ m/s}^2$

---

**7.2 Non-Uniform Circular Motion**
We are aware of the fact that the speed of a particle under circular motion is not constant.

A change in speed means that unequal length of arc ($s$) is covered in equal time intervals. It further means that the change in the velocity ($v$) of the particle is not limited to change in direction as in the case of UCM.

**Radial or centripetal acceleration.** Change in direction is due to radial acceleration (centripetal acceleration), which is given by $a_R = \frac{v^2}{r}$.

**Tangential acceleration:** The non-uniform circular motion basically involves a change in speed. This change is accounted by the tangential acceleration, which results due to a tangential force and which acts along the direction of velocity. $a_T = \frac{dv}{dt}$

**7.3 Relation between Angular and Linear Acceleration**
The relationship between angular and linear acceleration is shown hereunder.
$a_T = \frac{dv}{dt} = \frac{d^2 s}{dt^2} = \frac{d^2}{dt^2}(r\theta) = r\frac{d^2 \theta}{dt^2} = r\alpha$

**Illustration 15:** A particle, starting from the position (5 m, 0 m), is moving along a circular path about the origin in x-y plane. The angular position of the particle is a function of time as given here, $\theta = t^2 + 0.2t + 1$. Find (i) tangential acceleration (JEE MAIN)
**Sol:** Differentiate the expression for angular position with respect to time to get angular velocity. Tangential acceleration is the product of angular acceleration and the radius.
From the data on initial position of the particle, it is clear that the radius of the circle is 5 m.
(i) For determining tangential acceleration, we need to have expression of linear speed in time.
$v = \omega r = (2t + 0.2) \times 5 = 10t + 1$
We obtain tangential acceleration by differentiating the above function: $a_T = \frac{dv}{dt} = 10\text{ m/s}^2$

**Illustration 16:** At a particular instant, a particle is moving at a speed of 10 m/s on a circular path of radius 100 m. Its speed is increasing at the rate of 1 $\text{m/s}^2$. What is the acceleration of the particle? (JEE MAIN)
**Sol:** The acceleration of the particle is the vector sum of the centripetal acceleration and the tangential acceleration. The tangential acceleration is equal to the rate of change of speed.
The acceleration of a particle is the vector sum of mutually perpendicular radial and tangential accelerations. The magnitude of tangential acceleration given here is $1\text{ m/s}^2$. Now, the radial acceleration at the particular instant is
$a_R = \frac{v^2}{r} = \frac{10^2}{100} = 1\text{ m/s}^2$
Hence, the magnitude of the acceleration of the particle is: $a = |\mathbf{a}| = \sqrt{\left(a_T^2 + a_R^2\right)} = \sqrt{1^2 + 1^2} \text{ m/s}^2 = \sqrt{2} \text{ m/s}^2$

**Illustration 17:** Which of the following expressions represent the magnitude of centripetal acceleration?:
(A) $\left|\frac{d^2\mathbf{r}}{dt^2}\right|$
(B) $\left|\frac{d\mathbf{v}}{dt}\right|$
(C) $r\frac{d\theta}{dt}$
(D) None of these
(JEE MAIN)
**Sol:** The magnitude of centripetal acceleration depends on the square of the magnitude of velocity.

The expression $\left|\frac{d\mathbf{v}}{dt}\right|$ represents the magnitude of tangential acceleration. The differential $\frac{d\theta}{dt}$ represents the magnitude of angular velocity. The expression $r\frac{d\theta}{dt}$ represents the magnitude of tangential velocity and the expression $\frac{d^2\mathbf{r}}{dt^2}$ is second-order differentiation of position vector ($\mathbf{r}$). This is the actual expression of acceleration of a particle under motion. Hence, the expression $\left|\frac{d^2\mathbf{r}}{dt^2}\right|$ represents the magnitude of total or resultant acceleration.
Hence, option (d) alone is correct.

**Illustration 18:** A particle is executing circular motion. But the magnitude of velocity of the particle changes from zero to $(0.3\hat{i} + 0.4\hat{j})\text{ m/s}$ in a period of 1 second. The magnitude of average tangential acceleration is:
(A) $0.1\text{ m/s}^2$
(B) $0.2\text{ m/s}^2$
(C) $0.3\text{ m/s}^2$
(D) $0.5\text{ m/s}^2$
(JEE MAIN)
**Sol:** Tangential acceleration is equal to the rate of change of speed. Average tangential acceleration is change in speed divided by total time.

The magnitude of average tangential acceleration is the ratio of change in speed and time as given by: $a_T = \frac{\Delta v}{\Delta t}$
Now, $\Delta v = \sqrt{\left(0.3^2 + 0.4^2\right)} = \sqrt{0.25} = 0.5\text{ m/s}$; $a_T = 0.5\text{ m/s}^2$
Hence, option (d) alone is correct.

**CONCEPTS**
> Radial acceleration contributes in changing the direction of velocity of an object, but it does not affect the magnitude of velocity. However, tangential acceleration affects the speed of the object in motion.
> **Vaibhav Krishan (JEE 2009, AIR 22)**

**FORMULAE SHEET**

**(a) Projectile Motion**
Time of flight: $T = \frac{2u\sin\theta}{g}$

Horizontal range: $R = \frac{u^2\sin2\theta}{g}$

Maximum height: $H = \frac{u^2\sin^2\theta}{2g}$

Trajectory equation (equation of path):
$y = x\tan\theta - \frac{gx^2}{2u^2\cos^2\theta} = x\tan\theta\left(1 - \frac{x}{R}\right)$

Projection on an inclined plane
[Diagram showing Projection on an inclined plane]

**(b) Relative Motion**
$v_{AB}$ (velocity of A with respect to B) = $v_A - v_B$
$a_{AB}$ (acceleration of A with respect to B) = $a_A - a_B$
Relative motion along straight line = $x_{BA} = x_B - x_A$

**(c) Crossing River:** A boat or man in a river always moves in the direction of resultant velocity of velocity of boat (or man) and velocity of the river flow.
[Diagram showing Crossing River vectors]

**(d) Shortest Time:** Velocity along the river, $V_x = V_R$
Velocity perpendicular to the river, $V_y = V_{mR}$
The net speed is given by $V_m = \sqrt{V_{mR}^2 + V_R^2}$

**(e) Shortest Path:** Velocity along the river, $V_x = 0$
and velocity perpendicular to river $V_y = \sqrt{V_{mR}^2 - V_R^2}$
The net speed is given by $V_m = \sqrt{V_{mR}^2 - V_R^2}$
at an angle of $90^\circ$ with the river direction.
velocity $V_y$ is used only to cross the river, therefore time to cross the river,
$t = \frac{d}{V_y} = \frac{d}{\sqrt{V_{mR}^2 - V_R^2}}$ and velocity $V_x$ is zero, therefore, in this case the drift should be zero.
$V_R = V_{mR}\sin\theta = 0 \quad \text{or} \quad V_R = V_{mR}\sin\theta \quad \text{or} \quad \theta = \sin^{-1}\frac{V_R}{V_{mR}}$

**(f) Rain Problems:** $\vec{v}_{Rm} = \vec{v}_R - \vec{v}_m \quad \text{or} \quad v_{Rm} = \sqrt{v_R^2 + v_m^2}$

**(g) Circular Motion**
i. Average angular velocity $\omega_{\text{av}} = \frac{\theta_2 - \theta_1}{t_2 - t_1} = \frac{\Delta\theta}{\Delta t}$
ii. Instantaneous angular velocity $\omega = \frac{d\theta}{dt}$
iii. Average angular acceleration $\alpha_{\text{av}} = \frac{\omega_2 - \omega_1}{t_2 - t_1} = \frac{\Delta\omega}{\Delta t}$
iv. Instantaneous angular acceleration $\alpha = \frac{d\omega}{dt} = \omega\frac{d\omega}{d\theta}$
v. Relation between speed and angular velocity $v = r\omega$ and $v = \omega r$
vi. Tangential...

3. A ball is thrown with a velocity of $8 \text{ m/s}$ making an angle of $60^\circ$ with the horizontal. Its velocity will be perpendicular to initial velocity of projection after a time of ($g=10 \text{ m/s}^2$)
(a) $\frac{1.6}{\sqrt{3}} \text{ s}$
(b) $\frac{4}{\sqrt{3}} \text{ s}$
(c) $0.6 \text{ s}$
(d) $1.6\sqrt{3} \text{ s}$

4. The minimum and maximum velocities of a projectile are $10 \text{ m/s}$ and $20 \text{ m/s}$ respectively. The horizontal range and maximum height are respectively ($g = 10 \text{ m/s}^2$)
(a) $10\sqrt{3} \text{ m}, 20 \text{ m}$
(b) $20\sqrt{3} \text{ m}, 15 \text{ m}$
(c) $20 \text{ m}, 15 \text{ m}$
(d) $10\sqrt{3} \text{ m}, 10 \text{ m}$

15. A gun mounted on the top of a moving truck is aimed in the backward direction at angle of $30^\circ$ to the vertical. If the velocity of the gun is $4 \text{ m/s}$, the speed of the truck to send the bullet vertically up is
(a) $1 \text{ m/s}$
(b) $\frac{\sqrt{3}}{2} \text{ m/s}$
(c) $0.5 \text{ m/s}$
(d) $2 \text{ m/s}$

16. A body is projected with the same speed at two different angles such that the horizontal range is same in both the cases. the maximum height attained are $20 \text{ m}$ and $80 \text{ m}$ respectively in the above two cases, then the range is
(a) $120 \text{ m}$
(b) $20 \text{ m}$
(c) $160 \text{ m}$
(d) $40 \text{ m}$

17. Two second after projection, a projectile is moving at $30^\circ$ above the horizontal. After one more second it is moving horizontally. Angle of projection is ($g = 10 \text{ m/s}^2$)
(a) $0^\circ$
(b) $45^\circ$
(c) $60^\circ$
(d) $90^\circ$

18. A ball is projected at an angle of $30^\circ$ and $60^\circ$ to the horizontal with the same initial velocity in each case. Ratio of their time of flight is
(a) $1:1$
(b) $1:3$
(c) $1:\sqrt{3}$
(d) $2:\sqrt{3}$

19. In the above problem, ratio of maximum height is
(a) $1:1$
(b) $1:3$
(c) $1:\sqrt{3}$
(d) $2:\sqrt{3}$

20. In the above problem, ratio of ranges is
(a) $1:1$
(b) $1:3$
(c) $1:\sqrt{3}$
(d) $2:\sqrt{3}$

21. A particle of mass $1 \text{ kg}$ is projected at an angle $45^\circ$ to the horizontal with an initial velocity of $20 \text{ m/s}$. Change in momentum during its time of flight is
(a) $10\sqrt{2} \text{ kg m/s}$
(b) $20\sqrt{2} \text{ kg m/s}$
(c) $30\sqrt{2} \text{ kg m/s}$
(d) $40\sqrt{2} \text{ kg m/s}$

22. A bullet is fired with a velocity of $196 \text{ ms}^{-1}$ at an angle of $30^\circ$ with horizontal. Time of flight of the bullet is
(a) $10 \text{ s}$
(b) $20 \text{ s}$
(c) $30 \text{ s}$
(d) $40 \text{ s}$

23. A player kicks a foot ball obliquely at a speed of $20 \text{ m/s}$ so that its range is maximum. Another player at a distance of $24 \text{ m}$ away in the direction of kick starts running at that instant to catch the ball. Before the ball hits the ground to catch it, the speed with which the second player has to run is ($g=10 \text{ ms}^{-2}$)
(a) $4 \text{ ms}^{-1}$
(b) $4\sqrt{2} \text{ ms}^{-1}$
(c) $8\sqrt{2} \text{ ms}^{-1}$
(d) $8 \text{ ms}^{-1}$

24. For a projectile the range and maximum height are equal. The angle of projection is
(a) $45^\circ$
(b) $0^\circ$
(c) $76^\circ$
(d) $90^\circ$

25. A bullet fired at an angle of $15^\circ$ with the horizontal hits the ground $6 \text{ km}$ away. Keeping the same velocity of projection for bullet to attain a range of $12 \text{ km}$, the angle of projection is
(a) $15^\circ$
(b) $30^\circ$
(c) $45^\circ$
(d) $60^\circ$

5. If $4 \text{ seconds}$ be the time in which a projectile reaches a point P of its path and $5 \text{ seconds}$ the time from P till it reaches the horizontal plane through the point of projection. The height of P from the horizontal plane is
(a) $78.4 \text{ m}$
(b) $98 \text{ m}$
(c) $122.5 \text{ m}$
(d) $220.5 \text{ m}$

The speed of a projectile at the maximum height is half of its initial speed. Its horizontal range is
(a) $\frac{u^2}{\sqrt{3}g}$
(b) $\frac{2u^2}{\sqrt{3}g}$
(c) $\frac{\sqrt{3} u^2}{2 g}$
(d) $\frac{\sqrt{3}u^2}{g}$

28. A healthy young man standing at distance of $7 \text{ m}$ from a $11.8 \text{ m}$ high building sees a kid slipping from the top floor. His uniform speed of run to catch the kid at the arms height of $1.8 \text{ m}$ is
(a) $4.9 \text{ m/s}$
(b) $9.8 \text{ m/s}$
(c) $3.5 \text{ m/s}$
(d) $7 \text{ m/s}$

29. A marble travelling at $100 \text{ cm/s}$ rolls of the edge of a level table. It hits the floor $30 \text{ cm}$ away from the spot directly below the edge of the table. Height of the table is
(a) $44 \text{ cm}$
(b) $100 \text{ cm}$
(c) $30 \text{ cm}$
(d) $70 \text{ cm}$

30. A body is projected downwards at an angle of $30^\circ$ with the horizontal from the top of a building of height $300 \text{ m}$. Its initial speed is $40 \text{ m/s}$. Time taken by it to hit the ground is ($g = 10 \text{ m/s}^2$)
(a) $2 \text{ s}$
(b) $4 \text{ s}$
(c) $6 \text{ s}$
(d) $8 \text{ s}$

31. A ball rolling off the top of a staircase of each step with height H and width W, with an initial velocity U will just hit $n^{\text{th}}$ step. Then n
(a) $\frac{2U^2H^2}{gW}$
(b) $\frac{2U^2H^2}{gW^2}$
(c) $\frac{2U^2H}{gW^2}$
(d) $\frac{2UH^2}{W^2}$

32. In the above problem, if $\text{H} = 20\text{cm}, \text{W} = 30\text{cm}, \text{U} = 18 \text{ kmph}$, then $\text{n} =$ ($g=10 \text{ m/s}^2$)
(a) $11.1$
(b) $6.5$
(c) $8.3$
(d) $12.8$

33. A body of mass 'm' is projected horizontally with a velocity 'v' from the top of a tower of height 'h' and it reaches ground at a distance 'x' from the foot of a tower. If a second body of mass '2m' is projected horizontally from the top of a tower of height 2h, it reaches the ground at a distance '2x' from the tower. The horizontal velocity of second body is
(a) v
(b) 2v
(c) $\sqrt{2}v$
(d) $v/2$

34. From the top of a tower of height $78.4 \text{ m}$ two stones are projected horizontally with $10 \text{ m/s}$ and $20 \text{ m/s}$ in opposite directions. On reaching the ground, their separation is
(a) $120 \text{ m}$
(b) $100 \text{ m}$
(c) $200 \text{ m}$
(d) $150 \text{ m}$

35. An aeroplane is flying horizontally at a height of $980 \text{ m}$ with velocity $100 \text{ ms}^{-1}$ drops a food packet. A person on the ground is $414 \text{ m}$ ahead horizontally from the dropping point. At what velocity should he move so that he can catch the food packet.
(a) $50\sqrt{2} \text{ ms}^{-1}$
(b) $\frac{50}{\sqrt{2}} \text{ ms}^{-1}$
(c) $100 \text{ ms}^{-1}$
(d) $200 \text{ ms}^{-1}$

36. A body is projected horizontally from the top of a high tower with a speed of $20 \text{ ms}^{-1}$. After 4 seconds, the displacement of the body is ($g=10 \text{ ms}^{-2}$)
(a) $40 \text{ m}$
(b) $80 \text{ m}$
(c) $80\sqrt{2} \text{ m}$
(d) $\frac{80}{\sqrt{2}} \text{ m}$

37. A fighter plane flying horizontally at an altitude of $2 \text{ km}$ with speed of $540 \text{ kmph}$ passes directly over head an anti aircraft gun. If the gun can fire a bullet at the muzzles speed of $500 \text{ ms}^{-1}$, at what angle with the vertical the gun should fire the bullet so that the bullet hits the plane ?
(a) $\cos^{-1}\left(\frac{3}{10}\right)$
(b) $\sin^{-1}\left(\frac{3}{10}\right)$
(c) $\tan^{-1}\left(\frac{3}{10}\right)$
(d) $45^\circ$

38. A hose pipe lying on a ground shoots a stream of water upward at an angle of $60^\circ$ to the horizontal. The speed of water is $20 \text{ ms}^{-1}$ as it leaves the hose. It will strike a wall $10 \text{ m}$ away at a height of ($g=10 \text{ ms}^{-2}$)
(a) $10.5 \text{ m}$
(b) $12.32 \text{ m}$
(c) $10 \text{ m}$
(d) $20 \text{ m}$

39. A particle having a mass of $0.5 \text{ kg}$ is projected with a speed of $98 \text{ ms}^{-1}$ at an angle of $60^\circ$. The magnitude of change of momentum of the particle after $10 \text{ seconds}$ in N-S is
(a) $0.5$
(b) $49$
(c) $98$
(d) $490$

40. If the velocity of a particle at greatest height is $\sqrt{2/5}$ times of its velocity when it is at half of the greatest height. The angle of projection is
(a) $30^\circ$
(b) $37^\circ$
(c) $60^\circ$
(d) $45^\circ$

41. A projectile has initially the same horizontal velocity as it would acquired if it had moved from rest with uniform acceleration of $3 \text{ ms}^{-2}$ for $0.5 \text{ min}$. If the maximum height reached by it is $80 \text{ m}$, then the angle of projection is ($g=10 \text{ ms}^{-2}$)
(a) $\tan^{-1}(3)$
(b) $\tan^{-1}(3/2)$
(c) $\tan^{-1}(4/9)$
(d) $\sin^{-1}(4/9)$

42. A body is projected horizontally from the top of a hill with a velocity of $9.8 \text{ m/s}$. What time elapses before the vertical velocity is twice the horizontal velocity ?
(a) $0.5 \text{ sec}$
(b) $1 \text{ sec}$
(c) $2 \text{ sec}$
(d) $1.5 \text{ sec}$

43. A javelin thrown into air at an angle with the horizontal has range of $200 \text{ m}$. If the time of flight is $5 \text{ second}$, then the horizontal component of velocity of the projectile at the highest point of the trajectory is
(a) $40 \text{ m/s}$
(b) $0 \text{ m/s}$
(c) $9.8 \text{ m/s}$
(d) infinite

44. The horizontal range of a projectile is $4\sqrt{3}$ times the maximum height achieved by it, then the angle of projection is
(a) $30^\circ$
(b) $45^\circ$
(c) $60^\circ$
(d) $90^\circ$

45. A small particle of mass m is projected at an angle $\theta$ with the x-axis with an initial velocity $v_0$ in the x-y plane as shown in figure. At a time $t < \frac{v_0 \sin\theta}{g}$, the angular momentum of the particle is

[Image showing a projectile trajectory with x and y axes, angle of projection $\theta$, and initial velocity $v_0$]

(a) $-mg v_0 t^2 \cos\theta \hat{j}$
(b) $mg v_0 t \cos\theta \hat{k}$
(c) $-\frac{1}{2} mg v_0 t^2 \cos\theta \hat{k}$
(d) $\frac{1}{2} mg v_0 t^2 \cos\theta \hat{i}$

46. A particle of mass 'm' is projected with a velocity $v$ making an angle of $30^\circ$ with the horizontal. The magnitude of angular momentum of the projectile about the point of projection when the particle is at its maximum height 'H' is
(a) zero
(b) $\frac{mv^3}{\sqrt{2}g}$
(c) $\frac{\sqrt{3} mv^3}{16 g}$
(d) $\frac{\sqrt{3} mv^2}{2 g}$

47. A projectile is given an initial velocity of $(\hat{i} + 2\hat{j})\text{ m/s}$, where $\hat{i}$ is along the ground and $\hat{j}$ is along the vertical. If $g=10 \text{ m/s}^2$, the equation of its trajectory is
(a) $y = x - 5x^2$
(b) $y = 2x - 5x^2$
(c) $4y = 2x - 5x^2$
(d) $4y = 2x - 25x^2$

48. The horizontal range and maximum height attained by a projectile are R and H respectively. If a constant horizontal acceleration $a = g/4$ is imparted to the projectile due to wind, then its horizontal range and maximum height will be :
(a) $(R+H), \frac{H}{2}$
(b) $\left(R+\frac{H}{2}\right), 2H$
(c) $(R+2H), H$
(d) $(R+H), H$

49. With what minimum speed a particle be projected from origin so that it is able to pass through a given point $(30\text{m}, 40\text{m})$?
(a) $60 \text{ m/s}$
(b) $30 \text{ m/s}$
(c) $50 \text{ m/s}$
(d) $40 \text{ m/s}$

50. A body dropped from a height H above the ground strikes an inclined plane at a height h above the ground. As a result of the impact, the velocity of the body becomes horizontal. The body will take the maximum time to reach the ground if
(a) $h = \frac{H}{4}$
(b) $h = \frac{H}{2\sqrt{2}}$
(c) $h = \frac{H}{2}$
(d) $h = \frac{H}{\sqrt{2}}$

51. A shot is fired from a point at a distance of $200 \text{ m}$ from the foot of a tower $100 \text{ m}$ high so that it just passes over it horizontally. The direction of shot with horizontal is
(a) $30^\circ$
(b) $45^\circ$
(c) $60^\circ$

52. A gun fires two bullets at $60^\circ$ and $30^\circ$ with the horizontal. The bullets strike at same horizontal distance. The ratio of maximum height for the two bullets is in the ratio
(a) $2 : 1$
(b) $3 : 1$
(c) $4 : 1$
(d) $1 : 1$

53. A train is standing on a platform, a man inside a compartment of a train drops a stone. At the same instant train starts to move with constant acceleration. The path of the particle as seen by the person who drops the stone is
(a) Parabola
(b) Straight line for sometime & parabola for remaining time.
(c) Straight line
(d) Variable path that cannot be defined.

54. A particle is projected with some velocity u making an angle $60^\circ$ with horizontal on to an inclined plane making an angle $30^\circ$ with horizontal its range on the inclined plane is
(a) $\frac{u^2}{g}$
(b) $\frac{2u^2}{g}$
(c) $\frac{u^2}{3g}$
(d) $\frac{2u^2}{3g}$

55. Time taken by the projectile to reach from A to B is t. Then the distance AB is equal to :
[Image showing a projectile motion from A to B on an inclined plane. Incline angle is $30^\circ$. Projection angle from horizontal is $60^\circ$. A is the origin. B is on the incline. C is directly below B on the horizontal. Initial velocity is u.]
(a) $\frac{ut}{\sqrt{3}}$
(b) $\frac{\sqrt{3}ut}{2}$
(c) $\sqrt{3}ut$
(d) $2ut$

56. A particle is projected with a certain velocity at an angle $\alpha$ above the horizontal from the foot of an inclined plane of inclination $30^\circ$. If the particle strikes the plane normally then $\alpha$ is equal to :
(a) $30^\circ + \tan^{-1}\left(\frac{\sqrt{3}}{2}\right)$
(b) $45^\circ$
(c) $60^\circ$
(d) $30^\circ + \tan^{-1}(2\sqrt{3})$

57. A particle falling vertically from a height hits a plane surface inclined to horizontal at an angle $\theta$ with speed $v_0$ and rebounds elastically. The distance along the plane where it will hit second time.
(a) $\frac{4v_0^2}{g}\sin\theta$
(b) $\frac{2v_0^2}{g}\sin\theta$
(c) $\frac{v_0^2}{g}\sin\theta$
(d) $\frac{v_0^2}{g}$

58. A projectile is thrown at an angle of $30^\circ$ with a velocity at $10\text{m/s}$ the change in velocity during the time interval in which it reaches the highest point is
(a) $10 \text{ m/s}$
(b) $5 \text{ m/s}$
(c) $5\sqrt{3} \text{ m/s}$
(d) $10\sqrt{3} \text{ m/s}$

59. A particle is projected from the ground with an initial speed of v at an angle of projection q. the average velocity of the particles between its time of projection and time it reaches highest point of trajectory is
(a) $\frac{v}{2} \sqrt{1 + 2\cos^2\theta}$
(b) $\frac{v}{2} \sqrt{1 + 2\sin^2\theta}$
(c) $\frac{v}{2} \sqrt{1 + 3\cos^2\theta}$
(d) $v \cos\text{q}$

**LEVEL - 1 KEY**

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| **1-10** | (c) | (c) | (b) | (d) | (b) | (d) | (b) | (c) | (c) | (b) |
| **11-20** | (a) | (b) | (a) | (b) | (d) | (c) | (c) | (c) | (a) | (a) |
| **21-30** | (b) | (b) | (b) | (c) | (c) | (b) | (c) | (a) | (a) | (c) |
| **31-40** | (c) | (b) | (c) | (a) | (a) | (c) | (b) | (b) | (b) | (c) |
| **41-50** | (a) | (c) | (c) | (a) | (c) | (c) | (b) | (d) | (b) | (c) |
| **51-59** | (b) | (b) | (c) | (a) | (d) | (a) | (a) | (b) | (c) | |

**LEVEL - I**

1. A ball is thrown with a velocity of 'u' making an angle '$\theta$' with the horizontal. Its velocity vector is normal to initial velocity vector (u) after a time interval of
(a) $\frac{u\sin\theta}{g}$
(b) $\frac{u}{g\cos\theta}$
(c) $\frac{u}{g\sin\theta}$
(d) $\frac{u\cos\theta}{g}$

2. The maximum height reached by a projectile is 'h'. Its time of flight is
(a) $\sqrt{\frac{4h}{g}}$
(b) $\frac{8h}{g}$
(c) $\sqrt{\frac{8h}{g}}$
(d) $\sqrt{\frac{16h}{g}}$

3. Two paper screens A and B are separated by a distance of $100 \text{ m}$. A bullet pierces A and then B. The hole in B is $10 \text{ cm}$ below the hole in A. If the bullet is travelling horizontally at A, velocity of the bullet at A is ($g=9.8 \text{ m/s}^2$)
(a) $500 \text{ m/s}$
(b) $700 \text{ m/s}$
(c) $800 \text{ m/s}$
(d) $900 \text{ m/s}$

4. Two tall buildings are $80 \text{ m}$ apart. The velocity with which a ball should be thrown horizontally from a window $95 \text{ m}$ above the ground in one building so that it will enter a window $15 \text{ m}$ above the ground in the second building is ($g=10 \text{ m/s}^2$)
(a) $15 \text{ m/s}$
(b) $5 \text{ m/s}$
(c) $10 \text{ m/s}$
(d) $20 \text{ m/s}$

5. A particle projected from the level ground just clears in its ascent a wall $30 \text{ m}$ high and $120\sqrt{3}$ away measured horizontally. The time since projection to clear the wall is two second. It will strike the ground in the same horizontal plane from the wall on the other side at a distance of
(a) $150\sqrt{3} \text{ m}$
(b) $180\sqrt{3} \text{ m}$
(c) $120\sqrt{3} \text{ m}$
(d) $210\sqrt{3} \text{ m}$

6. A person projects a bottle into a dustbin at the same height as he is $2 \text{m}$ away at an angle of $45^\circ$. The velocity of projection is (in m/s)
(a) $g$
(b) $\sqrt{g}$
(c) $2g$
(d) $\sqrt{2g}$

7. A ball of mass 'm' is thrown vertically upwards. Another ball of mass '2m' is thrown up making an angle '$\theta$' with the vertical. Both of them stay in air for the same time. Their maximum heights are in the ratio
(a) $2:1$
(b) $1:1$
(c) $1:\cos\theta$
(d) $1:\sec\theta$

8. From the top of a building $80 \text{ m}$ high, a ball is thrown horizontally which hits the ground at a distance. The line joining the top of the building to the point where it hits the ground makes an angle of $45^\circ$ with the ground. Initial velocity of projection of the ball is ($g=10 \text{ m/s}^2$)
(a) $10 \text{ m/s}$
(b) $15 \text{ m/s}$
(c) $20 \text{ m/s}$
(d) $30 \text{ m/s}$

9. A stone is projected from the top of a tower with velocity $20 \text{ m/s}$ making an angle of elevation of $30^\circ$ with the horizontal. If the total time of flight is $5 \text{s}$ and $g = 10 \text{ ms}^{-2}$, then
(a) the height of the tower is $75 \text{m}$
(b) the maximum height of the stone from the ground is $80 \text{m}$
(c) both the above are true
(d) the height of the tower is $120 \text{m}$

10. A stone is projected with velocity $80 \text{ m/s}$ making an angle of $30^\circ$ with the horizontal. The horizontal component of its velocity after 2 second is ($g=10 \text{ ms}^{-2}$)
(a) $40 \text{ m/s}$
(b) $40\sqrt{3} \text{ m/s}$
(c) $20 \text{ m/s}$
(d) $20\sqrt{3} \text{ m/s}$

11. A body is projected at an angle of $30^\circ$ to the horizontal with a speed of $30 \text{ m/s}$. The angle made by the velocity with the horizontal after $1.5 \text{ s}$ is ($g=10 \text{ m/s}^2$)
(a) $0^\circ$
(b) $60^\circ$
(c) $45^\circ$
(d) $90^\circ$

12. A grass hopper can jump a maximum horizontal distance of $0.3 \text{ m}$. If it spends negligible time on the ground, its horizontal component of velocity is ($g=10 \text{ m/s}^2$)
(a) $3/2 \text{ m/s}$
(b) $\sqrt{\frac{3}{2}} \text{ m/s}$
(c) $1/2 \text{ m/s}$
(d) $\sqrt{\frac{2}{3}} \text{ m/s}$
