function matrix = reducematrix(vector,numrows)
vector = strsplit(vector, ' ');
numcols = length(vector) / numrows;
matrix = zeros(1,length(vector));
for n = 1:length(vector)
    matrix(n) = str2double(vector{n});
end
matrix = vec2mat(matrix,numcols);
matrix = rref(matrix);
end