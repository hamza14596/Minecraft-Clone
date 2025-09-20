layout(location = 0) in vec3 vertex_position

out vec3 local_position;

void main(void) {
    local_position = vertex_position
}