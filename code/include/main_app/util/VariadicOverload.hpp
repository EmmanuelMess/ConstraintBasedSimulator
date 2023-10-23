#pragma once

template<class... Ts>
struct VariadicOverload : Ts... { using Ts::operator()...; };
template<class... Ts>
VariadicOverload(Ts...) -> VariadicOverload<Ts...>;