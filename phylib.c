#include "phylib.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {

    phylib_object *object_p = malloc(sizeof(phylib_object));    //allocating memory for the object pointer

    if(object_p == NULL){   //test if malloc pointer fails
        return NULL;
    }

    object_p->type = PHYLIB_STILL_BALL;
    object_p->obj.still_ball.number = number;
    object_p->obj.still_ball.pos = *pos;

    return object_p;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) {

    phylib_object *object_p = malloc(sizeof(phylib_object));    //allocating memory for the object pointer

    if(object_p == NULL){   //test if malloc pointer fails
        return NULL;
    }

    object_p->type = PHYLIB_ROLLING_BALL;
    object_p->obj.rolling_ball.number = number;
    object_p->obj.rolling_ball.pos = *pos;
    object_p->obj.rolling_ball.vel = *vel;
    object_p->obj.rolling_ball.acc = *acc;

    return object_p;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {

    phylib_object *object_p = malloc(sizeof(phylib_object));    //allocating memory for the object pointer

    if(object_p == NULL){   //test if malloc pointer fails
        return NULL;
    }

    object_p->type = PHYLIB_HOLE;
    object_p->obj.hole.pos = *pos;

    return object_p;
}

phylib_object *phylib_new_hcushion( double y ) {

    phylib_object *object_p = malloc(sizeof(phylib_object));    //allocating memory for the object pointer

    if(object_p == NULL){   //test if malloc pointer fails
        return NULL;
    }

    object_p->type = PHYLIB_HCUSHION;
    object_p->obj.hcushion.y = y;

    return object_p;
}

phylib_object *phylib_new_vcushion( double x ) {

    phylib_object *object_p = malloc(sizeof(phylib_object));    //allocating memory for the object pointer

    if(object_p == NULL){   //test if malloc pointer fails
        return NULL;
    }

    object_p->type = PHYLIB_VCUSHION;
    object_p->obj.vcushion.x = x;

    return object_p;
}

phylib_table *phylib_new_table( void ) {

    phylib_table *table_str = malloc(sizeof(phylib_table));    //allocating memory for the object pointer

    if(table_str == NULL){   //test if malloc pointer fails
        return NULL;
    }

    table_str->time = 0.0;

    table_str->object[0] = phylib_new_hcushion(0.0);
    table_str->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table_str->object[2] = phylib_new_vcushion(0.0);
    table_str->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //creating variables for each holes with the coordinates
    phylib_coord hole1 = {0.0 , 0.0};
    table_str->object[4] = phylib_new_hole(&hole1);
    phylib_coord hole2 = {0.0 , PHYLIB_TABLE_LENGTH / 2};
    table_str->object[5] = phylib_new_hole(&hole2);
    phylib_coord hole3 = {0.0 , PHYLIB_TABLE_LENGTH};
    table_str->object[6] = phylib_new_hole(&hole3);
    phylib_coord hole4 = {PHYLIB_TABLE_WIDTH , 0.0};
    table_str->object[7] = phylib_new_hole(&hole4);
    phylib_coord hole5 = {PHYLIB_TABLE_WIDTH , PHYLIB_TABLE_LENGTH / 2};
    table_str->object[8] = phylib_new_hole(&hole5);
    phylib_coord hole6 = {PHYLIB_TABLE_WIDTH , PHYLIB_TABLE_LENGTH};
    table_str->object[9] = phylib_new_hole(&hole6);

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        table_str->object[i] = NULL;
    }
    
    return table_str;
}

// Utility Functions

void phylib_copy_object( phylib_object **dest, phylib_object **src ) {

    // phylib_object *object_p = (phylib_object *)malloc(sizeof(phylib_object));

    // if(object_p == NULL){   //test if malloc pointer fails
    //     return;
    // }    
    if(*src == NULL){
        *dest = NULL;
        return;
    }
    else{
        *dest = malloc(sizeof(phylib_object));
        memcpy(*dest, *src, sizeof(phylib_object));  //copies the content from the location pointed by "src"
    }

}

phylib_table *phylib_copy_table( phylib_table *table ) {

    phylib_table *new_table_str = malloc(sizeof(phylib_table));

    if(new_table_str == NULL){   //test if malloc pointer fails
        return NULL;
    }

    memcpy(new_table_str, table, sizeof(phylib_table));
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {  //copies each individual address ofthe object to the new memorylocation    
        if (new_table_str->object[i] != NULL) {
            phylib_copy_object(&new_table_str->object[i], &table->object[i]);
        }
        
    }
    new_table_str->time = table->time;  //copies the content of the table to the new memory location
 
    return new_table_str;
}

void phylib_add_object( phylib_table *table, phylib_object *object ) {

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] == NULL){   //assigning the address of the object to the null pointer
            table->object[i] = object;
            break;
        }
    }

    //if there's no null pointer ends the funtion
    
}

void phylib_free_table( phylib_table *table ) {

    if (table == NULL) {
        return;
    }
    

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){   //free the space in every null pointer
        if(table->object[i] != NULL){
            free(table->object[i]);
        }
    }

    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {

    //calculates the subtraction of two coordinates
    phylib_coord ans;

    ans.x = c1.x - c2.x;
    ans.y = c1.y - c2.y;

    return ans;
}

double phylib_length( phylib_coord c ) {

    //calculates the distance of an object
    double length;

    length = sqrt((c.x*c.x) + (c.y*c.y));

    return length;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {
    
    //calculates the dot product of two coordinates
    double dot_p;

    dot_p = (a.x*b.x) + (a.y*b.y);

    return dot_p;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {

    double length = 0.0;
    double hcushion_pos = 0.0; 
    double vcushion_pos = 0.0;
    phylib_coord c1 = obj1->obj.rolling_ball.pos;
    phylib_coord c2, hole_position;

    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }


    // the distance between the obj1 and obj2 if it's a still_ball
    if(obj2->type == PHYLIB_STILL_BALL) {
        c2 = obj2->obj.still_ball.pos;

        length = (phylib_length(phylib_sub(c1,c2))) - PHYLIB_BALL_DIAMETER;

        return length;
    }

    //the distance between the obj1 and obj2 if it's a rolling_ball
    else if (obj2->type == PHYLIB_ROLLING_BALL) {
        c2 = obj2->obj.rolling_ball.pos;

        length = (phylib_length(phylib_sub(c1,c2))) - PHYLIB_BALL_DIAMETER;

        return length;
    }

    // the distance between the obj1 and a hole
    else if (obj2->type == PHYLIB_HOLE) {
        hole_position = obj2->obj.hole.pos;

        length = (phylib_length(phylib_sub(c1,hole_position))) - PHYLIB_HOLE_RADIUS;
        return length;
    }

    // the distance between the obj1 and the Hcushion
    else if (obj2->type == PHYLIB_HCUSHION) {
        hcushion_pos = obj2->obj.hcushion.y;

        length = fabs(c1.y - hcushion_pos) - PHYLIB_BALL_RADIUS;
        return length;
    }

     // the distance between the obj1 and the Vcushion
    else if (obj2->type == PHYLIB_VCUSHION) {
        vcushion_pos = obj2->obj.vcushion.x;

        length = fabs(c1.x - vcushion_pos) - PHYLIB_BALL_RADIUS;
        return length;
    }
    else{
        return -1.0; // if obj2 isn't any valid type
    }
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ) {

    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    double newValX = new->obj.rolling_ball.vel.x;
    double newValY = new->obj.rolling_ball.vel.y;


    //Updating the values of the position of new in the x and y dimensions
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * time * time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * time * time;
    
    //Updating the values of the velocity of new in the x and y dimensions
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    // new->obj.rolling_ball.acc.x = old->obj.rolling_ball.acc.x;
    // new->obj.rolling_ball.acc.y = old->obj.rolling_ball.acc.y;

    //setting the velocity and acceleration to 0 if the signs changed
    if((new->obj.rolling_ball.vel.x * newValX) < 0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
        old->obj.rolling_ball.acc.x = 0.0;
    }
    if((new->obj.rolling_ball.vel.y * newValY) < 0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
        old->obj.rolling_ball.acc.y = 0.0;
    }
    
}

unsigned char phylib_stopped( phylib_object *object ) {

    //double speed = phylib_length(object->obj.rolling_ball.vel);
    // phylib_coord temp_pos = object->obj.rolling_ball.pos;
    // unsigned char temp_number = object->obj.rolling_ball.number;


    if (object->type != PHYLIB_ROLLING_BALL) {
        return 0;
    }
    if (object == NULL) {
        return 0;
    }

    // check if the ball has stopped
    if(phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        
        
        object->type = PHYLIB_STILL_BALL;   //converts the type to STILL_BALL

        //transferring the x and y positions and number to still ball
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        //printf("%d", object->obj.still_ball.number);

        return 1;
    }

    return 0;
}

void phylib_bounce( phylib_object **a, phylib_object **b ) {

    if ((*a)->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            //negating the velocity and acceleration
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;
        
        case PHYLIB_VCUSHION:
            //negating the velocity and acceleration
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;
        
        case PHYLIB_HOLE:
            //freeing the hole
            free(*a);
            *a = NULL;
            break;
        
        case PHYLIB_STILL_BALL:
            //assigning the object to rolling_ball
            (*b)->type = PHYLIB_ROLLING_BALL;

            int temp_number = (*b)->obj.still_ball.number;
            phylib_coord temp_pos = (*b)->obj.still_ball.pos;

            //setting up the object to be a rolling ball
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

            (*b)->obj.rolling_ball.number = temp_number;
            (*b)->obj.rolling_ball.pos = temp_pos;

        case PHYLIB_ROLLING_BALL: {
            //Position of a wrt b
            phylib_coord r_ab;
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            //relative velocity of a wrt b
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            
            //normal vector
            phylib_coord n;
            n.x = r_ab.x / phylib_length(r_ab);
            n.y = r_ab.y / phylib_length(r_ab);

            //ratio of the relative velocity
            double vel_rel_n;
            vel_rel_n = phylib_dot_product(v_rel, n);

            //Updating the x and y velocities of ball a
            (*a)->obj.rolling_ball.vel.x -= (vel_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y -= (vel_rel_n * n.y);

            //Updating the x and y velocities of ball b
            (*b)->obj.rolling_ball.vel.x += (vel_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y += (vel_rel_n * n.y);

            //speeds of a and b
            double a_speed, b_speed;
            a_speed = phylib_length((*a)->obj.rolling_ball.vel);
            b_speed = phylib_length((*b)->obj.rolling_ball.vel);

            //computing the speeds as the length of their velocities
            if (a_speed > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = (-((*a)->obj.rolling_ball.vel.x)/ a_speed) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (-((*a)->obj.rolling_ball.vel.y)/ a_speed) * PHYLIB_DRAG;
            }

            if(b_speed > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = (-((*b)->obj.rolling_ball.vel.x)/ b_speed) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = (-((*b)->obj.rolling_ball.vel.y)/ b_speed) * PHYLIB_DRAG;
            }
            break;
        }
    }
}

unsigned char phylib_rolling( phylib_table *t ) {

    unsigned char count = 0;

    //counting how many rollongballs are on the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if((t->object[i] != NULL) && (t->object[i]->type == PHYLIB_ROLLING_BALL)) {
            count++;
        }
    }
    
    return count;
}

phylib_table *phylib_segment( phylib_table *table ) {
    //printf("TEST1\n");
    if(phylib_rolling(table) == 0) {   //checks if there are any rolling ballson the table
        return NULL;
    }


    phylib_table *new_table = phylib_copy_table(table);
    double time = PHYLIB_SIM_RATE;

    do{
        //printf("Test\n");
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(new_table->object[i]!= NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {

                //rolling all the balls and checking if they stopped
                phylib_roll(new_table->object[i], table->object[i], time);
            }
        }
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {
                if (phylib_stopped(new_table->object[i])) {
                    new_table->time += time;
                    return new_table;
                }

                //bounce the balls off objects
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (j!=i && new_table->object[j]!= NULL && phylib_distance(new_table->object[i], new_table->object[j]) < 0.0) {
                        phylib_bounce(&(new_table->object[i]), &(new_table->object[j]));
                        new_table->time += time;
                        return new_table;
                    }
                
                }
            }
        }
        time += PHYLIB_SIM_RATE;
    } while(time < PHYLIB_MAX_TIME);
    new_table->time += time;
    return new_table;   
}


//New C Function
char *phylib_object_string( phylib_object *object ) {
    static char string[80]; 
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" ); 
        return string;
    }

    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
        snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x, 
            object->obj.still_ball.pos.y);
        break;

        case PHYLIB_ROLLING_BALL: 
        snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", 
            object->obj.rolling_ball.number, 
            object->obj.rolling_ball.pos.x, 
            object->obj.rolling_ball.pos.y, 
            object->obj.rolling_ball.vel.x, 
            object->obj.rolling_ball.vel.y, 
            object->obj.rolling_ball.acc.x, 
            object->obj.rolling_ball.acc.y);
        break;

        case PHYLIB_HOLE: 
        snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)", 
            object->obj.hole.pos.x, 
            object->obj.hole.pos.y );
        break;

        case PHYLIB_HCUSHION: 
        snprintf( string, 80,
            "HCUSHION (%6.1lf)", 
            object->obj.hcushion.y);
        break;

        case PHYLIB_VCUSHION: 
        snprintf( string, 80,
            "VCUSHION (%6.1lf)", 
            object->obj.vcushion.x);
        break;
    }
    return string;

}


